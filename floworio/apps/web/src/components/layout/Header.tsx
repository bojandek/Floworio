"use client";

import { motion } from "framer-motion";

export function Header() {
  return (
    <header className="border-b border-white/10 bg-dark-900/80 backdrop-blur-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        {/* Logo */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex items-center gap-3"
        >
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center text-white font-bold text-sm">
            F
          </div>
          <span className="text-xl font-bold gradient-text">floworio</span>
          <span className="text-xs text-dark-400 bg-dark-800 px-2 py-0.5 rounded-full border border-white/10">
            beta
          </span>
        </motion.div>

        {/* Nav */}
        <nav className="hidden md:flex items-center gap-6">
          <a href="#" className="text-sm text-dark-300 hover:text-white transition-colors">
            Examples
          </a>
          <a href="#" className="text-sm text-dark-300 hover:text-white transition-colors">
            Pricing
          </a>
          <a href="#" className="text-sm text-dark-300 hover:text-white transition-colors">
            Docs
          </a>
        </nav>

        {/* Actions */}
        <div className="flex items-center gap-3">
          <button className="text-sm text-dark-300 hover:text-white transition-colors px-3 py-1.5">
            Sign In
          </button>
          <button className="text-sm bg-brand-600 hover:bg-brand-500 text-white px-4 py-1.5 rounded-lg transition-colors font-medium">
            Get Started Free
          </button>
        </div>
      </div>
    </header>
  );
}
