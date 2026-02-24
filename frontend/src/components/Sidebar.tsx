import React from "react";
import type { QuickLink } from "../types";

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;

  activePage: string;
  setActivePage: (page: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({
  isOpen,
  onClose,
  activePage,
  setActivePage,
}) => {
  const quickLinks: QuickLink[] = [
    {
      id: "1",
      label: "Library",
      icon: "local_library",
      page: "library",
    },
    {
      id: "2",
      label: "Admissions",
      icon: "school",
      page: "admissions",
    },
    {
      id: "3",
      label: "Student Portal",
      icon: "badge",
      page: "portal",
    },
    {
      id: "4",
      label: "Contact Info",
      icon: "contact_phone",
      page: "contact",
    },
  ];

  const neuLogo =
    "https://lh3.googleusercontent.com/aida-public/AB6AXuCl1g9J4c4O2r9gnQx1VXbQU_GuVBfOtOujeGG7msemUlnpMTlF270M8n9QT8bm472BrrLdOp_aNRRErm7XhqcSDnBR8jyzMwW0EPkFG019VPo_t_I8N6tmoYPYvF9A1BJZqlTIxtboLCCEf9kB0sNonid7Q50DssoTlavEvLGi9M5iCGjmrUogftm3kSTwUEsF3ZaNFgn1D4WArVysmSqdHlEYn8uX4rJ6VOtBgwuPJcJvdkro-ow2nicfbrLjE2XlVQPvZrwrmW9N";

  return (
    <>
      {/* Overlay for mobile */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          w-64 flex flex-col bg-white border-r border-[#f4f0f0] h-full z-50
          fixed md:relative
          transition-transform duration-300 ease-in-out
          ${isOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"}
        `}
      >
        {/* Logo */}
        <div className="p-6 pb-2">
          <div className="flex items-center gap-3">
            <div
              className="bg-center bg-no-repeat bg-cover rounded-full size-10 shrink-0"
              style={{ backgroundImage: `url("${neuLogo}")` }}
            />
            <div>
              <h1 className="text-[#181111] text-base font-bold">NEU</h1>
              <p className="text-[#896161] text-xs uppercase tracking-wider">
                Student Resources
              </p>
            </div>
          </div>
        </div>

        {/* Links */}
        <nav className="flex-1 px-3 py-4 flex flex-col gap-2">
          {quickLinks.map((link) => {
            const isActive = activePage === link.page;

            return (
              <button
                key={link.id}
                onClick={() => {
                  setActivePage(link.page);
                  onClose(); // closes sidebar on mobile
                }}
                className={`
                  flex items-center gap-3 px-3 py-3 rounded-lg transition-colors w-full text-left
                  ${
                    isActive
                      ? "bg-primary/10 border border-primary/20"
                      : "hover:bg-[#f4f0f0]"
                  }
                `}
              >
                <span
                  className={`
                    material-symbols-outlined
                    ${isActive ? "text-primary" : "text-[#896161]"}
                  `}
                  style={{ fontSize: "24px" }}
                >
                  {link.icon}
                </span>

                <p
                  className={`text-sm font-medium ${
                    isActive ? "text-primary" : "text-[#181111]"
                  }`}
                >
                  {link.label}
                </p>
              </button>
            );
          })}
        </nav>

        {/* Bottom Settings */}
        <div className="p-4 border-t border-[#f4f0f0]">
          <button className="w-full flex items-center gap-3 px-3 py-2 hover:bg-[#f4f0f0] rounded-lg">
            <span
              className="material-symbols-outlined text-[#896161]"
              style={{ fontSize: "20px" }}
            >
              settings
            </span>
            <p className="text-[#896161] text-sm font-medium">Settings</p>
          </button>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
