"use client";

import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import toast from "react-hot-toast";
import { useProjectStore } from "@/store/projectStore";

interface UploadZoneProps {
  onComplete: () => void;
}

export function UploadZone({ onComplete }: UploadZoneProps) {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const { setProject } = useProjectStore();

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      const file = acceptedFiles[0];
      if (!file) return;

      if (!file.name.endsWith(".xlsx") && !file.name.endsWith(".xls") && !file.name.endsWith(".csv")) {
        toast.error("Please upload an Excel (.xlsx, .xls) or CSV file");
        return;
      }

      setUploading(true);
      setProgress(10);

      try {
        const formData = new FormData();
        formData.append("file", file);

        setProgress(30);

        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/upload`, {
          method: "POST",
          body: formData,
        });

        setProgress(70);

        if (!response.ok) {
          throw new Error("Upload failed");
        }

        const data = await response.json();
        setProgress(100);

        setProject({
          dataId: data.data_id,
          fileName: file.name,
          columns: data.columns,
          dateRange: data.date_range,
          status: "processing",
        });

        toast.success(`✅ ${file.name} uploaded successfully!`);
        setTimeout(() => onComplete(), 500);
      } catch (error) {
        toast.error("Upload failed. Make sure the API is running.");
        console.error(error);
      } finally {
        setUploading(false);
        setProgress(0);
      }
    },
    [setProject, onComplete]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"],
      "application/vnd.ms-excel": [".xls"],
      "text/csv": [".csv"],
    },
    maxFiles: 1,
    disabled: uploading,
  });

  return (
    <div className="max-w-3xl mx-auto">
      {/* Hero */}
      <div className="text-center mb-12">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          Turn your data into{" "}
          <span className="gradient-text">viral videos</span>
        </h1>
        <p className="text-dark-300 text-lg max-w-xl mx-auto">
          Upload your Excel data, and we&apos;ll generate an animated data story video
          with AI narration — ready to publish on TikTok, Instagram, and YouTube.
        </p>
      </div>

      {/* Upload Zone */}
      <div
        {...getRootProps()}
        className={`upload-zone rounded-2xl p-16 text-center cursor-pointer transition-all ${
          isDragActive ? "active" : ""
        } ${uploading ? "opacity-50 cursor-not-allowed" : ""}`}
      >
        <input {...getInputProps()} />

        {uploading ? (
          <div className="space-y-4">
            <div className="text-4xl animate-bounce">⏳</div>
            <p className="text-white font-medium">Processing your data...</p>
            <div className="w-full bg-dark-800 rounded-full h-2 max-w-xs mx-auto">
              <div
                className="progress-animated h-2 rounded-full transition-all duration-300"
                style={{ width: `${progress}%` }}
              />
            </div>
            <p className="text-dark-400 text-sm">{progress}%</p>
          </div>
        ) : isDragActive ? (
          <div className="space-y-3">
            <div className="text-5xl">📊</div>
            <p className="text-brand-400 font-medium text-lg">Drop it here!</p>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="text-5xl">📁</div>
            <div>
              <p className="text-white font-medium text-lg mb-1">
                Drag & drop your Excel file here
              </p>
              <p className="text-dark-400 text-sm">
                or click to browse — supports .xlsx, .xls, .csv
              </p>
            </div>
            <button className="mt-4 bg-brand-600 hover:bg-brand-500 text-white px-6 py-2.5 rounded-lg font-medium transition-colors">
              Choose File
            </button>
          </div>
        )}
      </div>

      {/* Data Format Info */}
      <div className="mt-8 glass rounded-xl p-6">
        <h3 className="text-sm font-semibold text-dark-300 mb-3 uppercase tracking-wider">
          📋 Expected Data Format
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-dark-400 border-b border-white/10">
                <th className="text-left py-2 pr-4">Date</th>
                <th className="text-left py-2 pr-4">Category 1</th>
                <th className="text-left py-2 pr-4">Category 2</th>
                <th className="text-left py-2">Category 3</th>
              </tr>
            </thead>
            <tbody className="text-dark-200">
              <tr className="border-b border-white/5">
                <td className="py-2 pr-4">2020</td>
                <td className="py-2 pr-4">1250</td>
                <td className="py-2 pr-4">890</td>
                <td className="py-2">2100</td>
              </tr>
              <tr className="border-b border-white/5">
                <td className="py-2 pr-4">2021</td>
                <td className="py-2 pr-4">1480</td>
                <td className="py-2 pr-4">1020</td>
                <td className="py-2">1950</td>
              </tr>
              <tr>
                <td className="py-2 pr-4">2022</td>
                <td className="py-2 pr-4">1720</td>
                <td className="py-2 pr-4">1340</td>
                <td className="py-2">2300</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p className="text-dark-500 text-xs mt-3">
          First column = dates (year, month, or full date). Each subsequent column = one data series.
        </p>
      </div>

      {/* Example datasets */}
      <div className="mt-6 text-center">
        <p className="text-dark-500 text-sm">
          Don&apos;t have data?{" "}
          <button className="text-brand-400 hover:text-brand-300 underline">
            Download example datasets
          </button>
        </p>
      </div>
    </div>
  );
}
