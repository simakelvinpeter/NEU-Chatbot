import React, { useState } from 'react';
import type { QuickLink } from '../types';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  const [quickLinks] = useState<QuickLink[]>([
    {
      id: '1',
      label: 'Library',
      icon: 'local_library',
      url: '#library',
      active: false,
    },
    {
      id: '2',
      label: 'Admissions',
      icon: 'school',
      url: '#admissions',
      active: false,
    },
    {
      id: '3',
      label: 'Student Portal',
      icon: 'badge',
      url: '#portal',
      active: true,
    },
    {
      id: '4',
      label: 'Contact Info',
      icon: 'contact_phone',
      url: '#contact',
      active: false,
    },
  ]);

  const neuLogo = 'https://lh3.googleusercontent.com/aida-public/AB6AXuCl1g9J4c4O2r9gnQx1VXbQU_GuVBfOtOujeGG7msemUlnpMTlF270M8n9QT8bm472BrrLdOp_aNRRErm7XhqcSDnBR8jyzMwW0EPkFG019VPo_t_I8N6tmoYPYvF9A1BJZqlTIxtboLCCEf9kB0sNonid7Q50DssoTlavEvLGi9M5iCGjmrUogftm3kSTwUEsF3ZaNFgn1D4WArVysmSqdHlEYn8uX4rJ6VOtBgwuPJcJvdkro-ow2nicfbrLjE2XlVQPvZrwrmW9N';

  return (
    <>
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden"
          onClick={onClose}
          aria-hidden="true"
        />
      )}
      <aside
        className={`
          w-64 flex flex-col bg-white border-r border-[#f4f0f0] shrink-0 h-full z-50
          fixed md:relative
          transition-transform duration-300 ease-in-out
          ${isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}
        `}
        aria-label="Sidebar navigation"
      >
        <div className="p-6 pb-2">
          <div className="flex items-center gap-3">
            <div
              className="bg-center bg-no-repeat bg-cover rounded-full size-10 shrink-0"
              style={{ backgroundImage: `url("${neuLogo}")` }}
              role="img"
              aria-label="Near East University Logo"
            />
            <div className="flex flex-col">
              <h1 className="text-[#181111] text-base font-bold leading-normal">
                NEU
              </h1>
              <p className="text-[#896161] text-xs font-normal leading-normal uppercase tracking-wider">
                Student Resources
              </p>
            </div>
          </div>
        </div>
        <nav
          className="flex-1 overflow-y-auto px-3 py-4 flex flex-col gap-2"
          aria-label="Quick links"
        >
          {quickLinks.map((link) => (
            <a
              key={link.id}
              href={link.url}
              className={`
                flex items-center gap-3 px-3 py-3 rounded-lg transition-colors group
                ${
                  link.active
                    ? 'bg-primary/5 border border-primary/10'
                    : 'hover:bg-[#f4f0f0]'
                }
              `}
              aria-current={link.active ? 'page' : undefined}
            >
              <span
                className={`
                  material-symbols-outlined
                  ${
                    link.active
                      ? 'text-primary'
                      : 'text-[#896161] group-hover:text-primary'
                  }
                `}
                style={{ fontSize: '24px' }}
                aria-hidden="true"
              >
                {link.icon}
              </span>
              <p
                className={`
                  text-sm font-medium leading-normal
                  ${link.active ? 'text-primary' : 'text-[#181111]'}
                `}
              >
                {link.label}
              </p>
            </a>
          ))}
        </nav>
        <div className="p-4 border-t border-[#f4f0f0]">
          <button
            className="w-full flex items-center gap-3 px-3 py-2 cursor-pointer hover:bg-[#f4f0f0] rounded-lg transition-colors"
            aria-label="Settings"
          >
            <span
              className="material-symbols-outlined text-[#896161]"
              style={{ fontSize: '20px' }}
              aria-hidden="true"
            >
              settings
            </span>
            <p className="text-[#896161] text-sm font-medium leading-normal">
              Settings
            </p>
          </button>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
