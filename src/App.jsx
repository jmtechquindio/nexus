import { Shield, Zap, MessageSquare, Brain, TrendingUp, BarChart3 } from 'lucide-react'
import { useState } from 'react'
import AnimatedCounter from './components/AnimatedCounter'

export default function App() {
  return (
    <div>
      <section className="min-h-screen flex flex-col justify-center items-center text-center px-6">
        <div className="inline-flex items-center gap-2 bg-gray-900/60 px-4 py-2 rounded-full mb-6">
          <Shield size={16} /> Transformación digital con IA
        </div>
        <h1 className="text-4xl md:text-6xl font-bold mb-4">
          Inteligencia Artificial y Automatización para Escalar Negocios
        </h1>
        <p className="text-gray-400 max-w-2xl">
          Diseñamos soluciones de IA que optimizan procesos, reducen costos y mejoran la toma de decisiones.
        </p>
        <button className="mt-8 bg-blue-600 hover:bg-blue-500 transition px-6 py-3 rounded-lg">
          Solicitar diagnóstico gratuito
        </button>
      </section>

      <section className="py-20 bg-gray-900">
        <div className="max-w-5xl mx-auto grid md:grid-cols-3 gap-8 text-center">
          <div>
            <AnimatedCounter value={40} suffix="%" />
            <p className="text-gray-400 mt-2">Reducción de costos</p>
          </div>
          <div>
            <AnimatedCounter value={60} suffix="%" />
            <p className="text-gray-400 mt-2">Ahorro de tiempo</p>
          </div>
          <div>
            <AnimatedCounter value={24} />
            <p className="text-gray-400 mt-2">Disponibilidad 24/7</p>
          </div>
        </div>
      </section>

      <section className="py-20 max-w-6xl mx-auto px-6 grid md:grid-cols-3 gap-6">
        {[
          { icon: Zap, title: 'Automatización de procesos' },
          { icon: MessageSquare, title: 'Agentes IA' },
          { icon: Brain, title: 'IA aplicada al negocio' },
          { icon: TrendingUp, title: 'Automatización comercial' },
          { icon: BarChart3, title: 'Consultoría estratégica' }
        ].map((s, i) => (
          <div key={i} className="bg-gray-900 p-6 rounded-xl hover:border-blue-500 border border-gray-800 transition">
            <s.icon className="text-blue-500 mb-4" />
            <h3 className="font-semibold">{s.title}</h3>
          </div>
        ))}
      </section>

      <footer className="py-10 text-center border-t border-gray-800">
        <h3 className="font-bold text-xl">Nexus AI</h3>
        <p className="text-gray-400">Agencia de Inteligencia Artificial</p>
        <a href="tel:+573212257107" className="text-blue-400 block mt-2">321 225 7107</a>
      </footer>
    </div>
  )
}
