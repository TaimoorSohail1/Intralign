import Image from "next/image";

export function BrandLockup() {
  return (
    <div className="brand-lockup" aria-label="Intralign OSLO">
      <Image alt="Intralign" className="brand-logo" height={22} priority src="/intralign-logo.webp" width={124} />
      <div className="brand-subtitle">OSLO · Strategic project leadership</div>
    </div>
  );
}
