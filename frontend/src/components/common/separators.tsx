export function OnionSeparator() {
  return (
    <div
      className="h-px w-full"
      style={{
        background:
          'linear-gradient(90deg, transparent 0%, oklch(0.48 0.12 340) 30%, oklch(0.55 0.12 340) 50%, oklch(0.48 0.12 340) 70%, transparent 100%)',
        boxShadow:
          '0 -2px 8px oklch(0.48 0.12 340 / 0.5), 0 -1px 3px oklch(0.48 0.12 340 / 0.7), 0 1px 8px oklch(0.48 0.12 340 / 0.3)',
      }}
    />
  );
}

export function LettuceSeparator() {
  return (
    <div
      className="h-px w-full"
      style={{
        background:
          'linear-gradient(90deg, transparent 0%, oklch(0.48 0.14 135) 30%, oklch(0.58 0.14 135) 50%, oklch(0.48 0.14 135) 70%, transparent 100%)',
        boxShadow:
          '0 -2px 8px oklch(0.48 0.14 135 / 0.5), 0 -1px 3px oklch(0.48 0.14 135 / 0.7), 0 1px 8px oklch(0.48 0.14 135 / 0.3)',
      }}
    />
  );
}
