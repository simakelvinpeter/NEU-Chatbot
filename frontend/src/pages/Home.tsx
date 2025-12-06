import React, { useState } from 'react';
import Sidebar from '../components/Sidebar';
import ChatWindow from '../components/ChatWindow';

const Home: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [onlineStatus] = useState(true);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const closeSidebar = () => {
    setSidebarOpen(false);
  };

  return (
    <div className="relative flex h-full w-full bg-white overflow-hidden">
      <Sidebar isOpen={sidebarOpen} onClose={closeSidebar} />
      <main className="flex-1 flex flex-col h-full relative min-w-0">
        <header className="flex items-center justify-between whitespace-nowrap border-b border-solid border-b-[#e5e0e0] bg-white px-6 py-4 shadow-sm z-10">
          <div className="flex items-center gap-4 text-[#181111]">
            <button
              onClick={toggleSidebar}
              className="md:hidden text-[#896161] p-2 hover:bg-[#f4f0f0] rounded-lg transition-colors"
              aria-label="Toggle menu"
            >
              <span className="material-symbols-outlined">menu</span>
            </button>
            <div className="flex flex-col">
              <h2 className="text-[#181111] text-lg font-bold leading-tight tracking-[-0.015em]">
                NEU Virtual Assistant
              </h2>
              <div className="flex items-center gap-1.5 mt-0.5">
                <span
                  className={`block w-2 h-2 rounded-full ${
                    onlineStatus ? 'bg-green-500' : 'bg-gray-400'
                  }`}
                  aria-hidden="true"
                />
                <span className="text-xs text-[#896161] font-medium">
                  {onlineStatus ? 'Online' : 'Offline'}
                </span>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <button
              aria-label="Notifications"
              className="flex items-center justify-center rounded-lg h-10 w-10 bg-[#f4f0f0] hover:bg-[#ebe7e7] text-[#181111] transition-colors"
            >
              <span
                className="material-symbols-outlined text-[#181111]"
                style={{ fontSize: '20px' }}
              >
                notifications
              </span>
            </button>
            <div
              className="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10 ring-2 ring-white shadow-sm cursor-pointer"
              style={{
                backgroundImage: `url("https://lh3.googleusercontent.com/aida-public/AB6AXuAslkr_mmxj5FWj6eNZ6uNw6prbjZkRA7Mp9uPOqM5CufNfaVVHNj87aYn3aK0iam1Zip7TeSO-HC7vi_2HLxJvNYOyoXIzxx6sIdSFSFlB_E_-kUigbNZTPQd3CkOoK_ITMFueLORUmSj-wp3lTnHOxE3J0gMiVatyHiywMVBCgdLd16zKPE7x36tLYChnep9YdSYyDa3TvcrLKuxzoqLTg288sHO-skpY_VzdF2JVKlXHkvRCab_Nl5alqje68dHeUL7IrVea3AhS")`,
              }}
              role="img"
              aria-label="User avatar"
            />
          </div>
        </header>
        <ChatWindow />
      </main>
    </div>
  );
};

export default Home;
