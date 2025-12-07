import React, { useState } from 'react';
import Sidebar from '../components/Sidebar';
import ChatWindow from '../components/ChatWindow';
import { Button, IconButton, Avatar, Tooltip } from '@mui/material';
import DeleteSweepIcon from '@mui/icons-material/DeleteSweep';
import MenuIcon from '@mui/icons-material/Menu';

const Home: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [onlineStatus] = useState(true);
  const [language, setLanguage] = useState<'EN' | 'TR'>('EN');
  const [clearChatTrigger, setClearChatTrigger] = useState(0);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const closeSidebar = () => {
    setSidebarOpen(false);
  };

  const handleClearChat = () => {
    setClearChatTrigger(prev => prev + 1);
  };

  return (
    <div className="relative flex h-screen w-full bg-white overflow-hidden">
      <Sidebar isOpen={sidebarOpen} onClose={closeSidebar} />
      <main className="flex-1 flex flex-col h-screen relative min-w-0">
        <header className="flex-shrink-0 flex items-center justify-between whitespace-nowrap border-b border-solid border-b-[#e5e0e0] bg-white px-6 py-4 shadow-sm z-50 sticky top-0">
          <div className="flex items-center gap-4 text-[#181111]">
            <Tooltip title="Menu">
              <IconButton
                onClick={toggleSidebar}
                className="md:hidden"
                sx={{ color: '#896161' }}
              >
                <MenuIcon />
              </IconButton>
            </Tooltip>
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
            <Button
              onClick={handleClearChat}
              startIcon={<DeleteSweepIcon />}
              variant="outlined"
              sx={{
                color: '#181111',
                borderColor: '#e5e0e0',
                backgroundColor: '#f4f0f0',
                textTransform: 'none',
                borderRadius: '8px',
                '&:hover': {
                  backgroundColor: '#ebe7e7',
                  borderColor: '#d4d0d0',
                },
              }}
            >
              Clear Chat
            </Button>

            <Tooltip title="User Profile">
              <Avatar
                src="https://lh3.googleusercontent.com/aida-public/AB6AXuAslkr_mmxj5FWj6eNZ6uNw6prbjZkRA7Mp9uPOqM5CufNfaVVHNj87aYn3aK0iam1Zip7TeSO-HC7vi_2HLxJvNYOyoXIzxx6sIdSFSFlB_E_-kUigbNZTPQd3CkOoK_ITMFueLORUmSj-wp3lTnHOxE3J0gMiVatyHiywMVBCgdLd16zKPE7x36tLYChnep9YdSYyDa3TvcrLKuxzoqLTg288sHO-skpY_VzdF2JVKlXHkvRCab_Nl5alqje68dHeUL7IrVea3AhS"
                alt="User avatar"
                sx={{
                  width: 40,
                  height: 40,
                  border: '2px solid white',
                  boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
                  cursor: 'pointer',
                }}
              />
            </Tooltip>
          </div>
        </header>
        <ChatWindow clearChatTrigger={clearChatTrigger} language={language} />
      </main>
    </div>
  );
};

export default Home;
