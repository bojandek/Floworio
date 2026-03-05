'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { ArrowRight, Zap, Sparkles, Rocket } from 'lucide-react';

const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.6 },
};

const staggerContainer = {
  animate: {
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2,
    },
  },
};

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-md z-50 border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="text-2xl font-bold text-black">
            <span className="bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
              Floworio
            </span>
          </div>
          <div className="flex gap-8 items-center">
            <a href="#how-it-works" className="text-gray-600 hover:text-black transition">
              How it works
            </a>
            <a href="#pricing" className="text-gray-600 hover:text-black transition">
              Pricing
            </a>
            <Link
              href="/dashboard"
              className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
            >
              Get Started
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-6 bg-gradient-to-b from-black via-black to-white">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-6xl md:text-7xl font-bold text-white mb-6 leading-tight">
              Type a topic.
              <br />
              <span className="bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
                Get a viral video.
              </span>
              <br />
              In 60 seconds.
            </h1>
          </motion.div>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto"
          >
            Upload your data. AI writes the story. Remotion renders the video. 
            Publish to TikTok, Instagram, YouTube in one click.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="flex gap-4 justify-center mb-12"
          >
            <Link
              href="/dashboard"
              className="px-8 py-4 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition flex items-center gap-2 font-semibold"
            >
              Start free. No credit card.
              <ArrowRight size={20} />
            </Link>
            <button className="px-8 py-4 border border-gray-400 text-white rounded-lg hover:border-white transition font-semibold">
              Watch demo
            </button>
          </motion.div>

          {/* Demo Video Placeholder */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="relative aspect-video bg-gray-900 rounded-2xl overflow-hidden border border-gray-800 shadow-2xl"
          >
            <div className="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-gray-900 to-black">
              <div className="text-center">
                <div className="w-20 h-20 bg-indigo-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Rocket className="text-white" size={40} />
                </div>
                <p className="text-gray-400">Demo video coming soon</p>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="py-20 px-6 bg-white">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-5xl font-bold text-black mb-4">Three simple steps</h2>
            <p className="text-xl text-gray-600">From data to viral video in minutes</p>
          </motion.div>

          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="grid md:grid-cols-3 gap-8"
          >
            {[
              {
                icon: <Zap className="text-indigo-600" size={32} />,
                title: 'Upload your data',
                description: 'Excel, CSV, or paste data. We handle the rest.',
              },
              {
                icon: <Sparkles className="text-indigo-600" size={32} />,
                title: 'AI writes the story',
                description: 'GPT-4 analyzes trends and writes compelling narration.',
              },
              {
                icon: <Rocket className="text-indigo-600" size={32} />,
                title: 'Publish everywhere',
                description: 'One click to TikTok, Instagram, YouTube, LinkedIn.',
              },
            ].map((step, i) => (
              <motion.div
                key={i}
                variants={fadeInUp}
                className="p-8 rounded-xl border border-gray-200 hover:border-indigo-300 transition bg-gray-50"
              >
                <div className="mb-4">{step.icon}</div>
                <h3 className="text-xl font-semibold text-black mb-2">{step.title}</h3>
                <p className="text-gray-600">{step.description}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="py-20 px-6 bg-gray-50">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-5xl font-bold text-black mb-4">Simple pricing</h2>
            <p className="text-xl text-gray-600">Choose the plan that fits your needs</p>
          </motion.div>

          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="grid md:grid-cols-4 gap-6"
          >
            {[
              {
                name: 'Free',
                price: '$0',
                videos: '3 videos/month',
                platforms: '1 platform',
                features: ['Basic charts', 'Template stories', 'No voiceover'],
              },
              {
                name: 'Creator',
                price: '$29',
                videos: '30 videos/month',
                platforms: '3 platforms',
                features: ['All charts', 'AI stories', 'Kokoro TTS', 'Custom colors'],
                popular: true,
              },
              {
                name: 'Pro',
                price: '$79',
                videos: '150 videos/month',
                platforms: 'All platforms',
                features: ['Everything in Creator', 'Priority rendering', 'Analytics', 'API access'],
              },
              {
                name: 'Agency',
                price: '$199',
                videos: 'Unlimited',
                platforms: 'All platforms',
                features: ['Everything in Pro', 'Team accounts', 'White label', 'Dedicated support'],
              },
            ].map((plan, i) => (
              <motion.div
                key={i}
                variants={fadeInUp}
                className={`p-8 rounded-xl border transition ${
                  plan.popular
                    ? 'border-indigo-600 bg-white shadow-lg scale-105'
                    : 'border-gray-200 bg-white hover:border-indigo-300'
                }`}
              >
                {plan.popular && (
                  <div className="text-indigo-600 text-sm font-semibold mb-2">MOST POPULAR</div>
                )}
                <h3 className="text-2xl font-bold text-black mb-2">{plan.name}</h3>
                <div className="mb-4">
                  <span className="text-4xl font-bold text-black">{plan.price}</span>
                  <span className="text-gray-600">/month</span>
                </div>
                <div className="space-y-2 mb-6 text-sm text-gray-600">
                  <p>{plan.videos}</p>
                  <p>{plan.platforms}</p>
                </div>
                <ul className="space-y-2 mb-6">
                  {plan.features.map((feature, j) => (
                    <li key={j} className="text-sm text-gray-700 flex items-center gap-2">
                      <span className="text-indigo-600">✓</span> {feature}
                    </li>
                  ))}
                </ul>
                <button
                  className={`w-full py-2 rounded-lg font-semibold transition ${
                    plan.popular
                      ? 'bg-indigo-600 text-white hover:bg-indigo-700'
                      : 'border border-gray-300 text-black hover:border-indigo-600'
                  }`}
                >
                  Get started
                </button>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* CTA Footer */}
      <section className="py-20 px-6 bg-black text-white">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl font-bold mb-6">Ready to create?</h2>
            <p className="text-xl text-gray-300 mb-8">
              Join creators who are turning data into viral videos.
            </p>
            <Link
              href="/dashboard"
              className="inline-block px-8 py-4 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition font-semibold"
            >
              Start free. No credit card.
            </Link>
          </motion.div>
        </div>
      </section>
    </div>
  );
}
