import { useEffect, useRef, useState } from "react"

export default function AnimatedCounter({ value, suffix = "" }) {
  const ref = useRef(null)
  const [count, setCount] = useState(0)
  const [started, setStarted] = useState(false)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => entry.isIntersecting && setStarted(true),
      { threshold: 0.6 }
    )
    if (ref.current) observer.observe(ref.current)
    return () => observer.disconnect()
  }, [])

  useEffect(() => {
    if (!started) return
    let current = 0
    const step = value / 60
    const tick = () => {
      current += step
      if (current < value) {
        setCount(Math.floor(current))
        requestAnimationFrame(tick)
      } else setCount(value)
    }
    requestAnimationFrame(tick)
  }, [started, value])

  return <span ref={ref} className="text-4xl font-bold">{count}{suffix}</span>
}
