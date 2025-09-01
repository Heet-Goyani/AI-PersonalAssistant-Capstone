import React from "react";

export default function Button({ variant = "default", size = "default", className = "", children, ...props }) {
  const base =
    "inline-flex items-center justify-center font-semibold rounded-lg transition focus:outline-none focus:ring-2 focus:ring-accent-neon/60";
  const variants = {
    default: "bg-primary text-white hover:bg-primary-dark",
    secondary: "bg-background-glass text-accent-neon border border-accent-neon/40 hover:bg-accent-neon/10",
    outline: "border border-primary text-primary bg-transparent hover:bg-primary/10",
    ai: "bg-gradient-to-r from-primary to-accent-neon text-white shadow-neon hover:from-accent-neon hover:to-primary",
    glow: "bg-accent-neon text-white shadow-neon hover:bg-primary-dark",
  };
  const sizes = {
    default: "px-5 py-2 text-base",
    sm: "px-3 py-1.5 text-sm",
    lg: "px-7 py-3 text-lg",
    icon: "p-2 text-xl w-12 h-12",
  };
  return (
    <button
      className={`${base} ${variants[variant] || variants.default} ${sizes[size] || sizes.default} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}
