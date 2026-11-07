import { ButtonHTMLAttributes } from "react";

type ButtonVariant = "default" | "primary" | "danger";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
}

export function Button({ variant = "default", children, ...rest }: ButtonProps) {
  return (
    <button className={`btn-${variant}`} {...rest}>
      {children}
    </button>
  );
}
