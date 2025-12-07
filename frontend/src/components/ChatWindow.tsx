import React, { useState, useRef, useEffect } from 'react';
import MessageBubble from './MessageBubble';
import { sendMessage } from '../utils/api';
import type { Message } from '../types';
import { TextField, IconButton, CircularProgress, Chip, Box, Tooltip } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import AttachFileIcon from '@mui/icons-material/AttachFile';

interface ChatWindowProps {
  clearChatTrigger: number;
  language: 'EN' | 'TR';
}

const ChatWindow: React.FC<ChatWindowProps> = ({ clearChatTrigger, language }) => {
  const initialMessage: Message = {
    id: '1',
    content: language === 'EN' 
      ? 'Hello! I am the NEU Virtual Assistant. How can I help you today?'
      : 'Merhaba! Ben NEU Sanal Asistanıyım. Bugün size nasıl yardımcı olabilirim?',
    sender: 'bot',
    timestamp: new Date(),
  };

  const [messages, setMessages] = useState<Message[]>([initialMessage]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string>('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  const quickActions = language === 'EN' ? [
    "How do I register?",
    "Tuition fees",
    "Campus map",
    "Scholarships",
    "Dormitories",
    "Faculties"
  ] : [
    "Nasıl kayıt olurum?",
    "Öğrenim ücreti",
    "Kampüs haritası",
    "Burslar",
    "Yurtlar",
    "Fakülteler"
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (clearChatTrigger > 0) {
      const newInitialMessage: Message = {
        id: '1',
        content: language === 'EN' 
          ? 'Hello! I am the NEU Virtual Assistant. How can I help you today?'
          : 'Merhaba! Ben NEU Sanal Asistanıyım. Bugün size nasıl yardımcı olabilirim?',
        sender: 'bot',
        timestamp: new Date(),
      };
      setMessages([newInitialMessage]);
      setSessionId('');
    }
  }, [clearChatTrigger, language]);

  useEffect(() => {
    const newInitialMessage: Message = {
      id: '1',
      content: language === 'EN' 
        ? 'Hello! I am the NEU Virtual Assistant. How can I help you today?'
        : 'Merhaba! Ben NEU Sanal Asistanıyım. Bugün size nasıl yardımcı olabilirim?',
      sender: 'bot',
      timestamp: new Date(),
    };
    setMessages([newInitialMessage]);
  }, [language]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await sendMessage(inputValue, sessionId, language);

      if (response.session_id) {
        setSessionId(response.session_id);
      }

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response.message,
        sender: 'bot',
        timestamp: new Date(response.timestamp),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: 'Sorry, I encountered an error. Please try again.',
        sender: 'bot',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
      console.error('Failed to send message:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileAttachment = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      console.log('File selected:', file.name);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputValue(e.target.value);
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 128)}px`;
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(e);
    }
  };

  const formatTimestamp = (date: Date) => {
    return new Intl.DateTimeFormat('en-US', {
      hour: 'numeric',
      minute: 'numeric',
      hour12: true,
    }).format(date);
  };

  return (
    <div className="flex-1 flex flex-col h-full relative min-w-0 bg-background-light">
      <div className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6 scroll-smooth">
        <div className="flex justify-center">
          <span className="text-xs font-medium text-[#896161]/60 bg-[#e5e0e0]/30 px-3 py-1 rounded-full">
            Today, {formatTimestamp(new Date())}
          </span>
        </div>
        
        {messages.length === 1 && (
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, justifyContent: 'center', mt: 2 }}>
            {quickActions.map((action) => (
              <Chip
                key={action}
                label={action}
                onClick={() => setInputValue(action)}
                clickable
                sx={{
                  backgroundColor: '#f4f0f0',
                  '&:hover': {
                    backgroundColor: '#ebe7e7',
                  },
                  fontSize: '0.8rem',
                  fontWeight: 500,
                }}
              />
            ))}
          </Box>
        )}
        
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
        {isLoading && (
          <div className="flex items-end gap-3 max-w-[85%]">
            <div
              className="bg-center bg-no-repeat aspect-square bg-cover rounded-full w-10 h-10 shrink-0 shadow-sm"
              style={{
                backgroundImage: `url("https://lh3.googleusercontent.com/aida-public/AB6AXuAGI0he52DtXffWJdVpjIdaUuTS-LYudDHB8OKoIFMWGXf-XJdmebDtfUX3TL0Y9sZTuo9wIOaOrpGyaGxqYzQETi1RHvy6tWO-nWfuzLwdJyuoiJVZVsxQdvY_u9epdCyIq7HOpzJsW9Ue6KV6hb-sExb4ZRpuO7gQJSW43Km1k-gpffnajdT3tSe-SgP_2_TcFaYB5AGft5TIw1OxEiI3YPgcrhF-GqNDwvvgLSLrco5tTK46D7xABjMNkVtD_73vmNRh7EMUw2Qg")`,
              }}
              role="img"
              aria-label="NEU Bot avatar"
            />
            <div className="flex flex-col gap-1 items-start">
              <span className="text-[#896161] text-xs font-medium ml-1">NEU Bot</span>
              <div className="text-base font-normal leading-relaxed rounded-2xl rounded-bl-none px-5 py-3 bg-white text-[#181111] shadow-sm border border-[#f0f0f0]">
                <div className="flex gap-1">
                  <span className="animate-bounce">●</span>
                  <span className="animate-bounce delay-100">●</span>
                  <span className="animate-bounce delay-200">●</span>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="p-4 bg-white border-t border-[#f4f0f0] w-full">
        <div className="max-w-[960px] mx-auto w-full">
          <form onSubmit={handleSendMessage}>
            <Box sx={{ display: 'flex', alignItems: 'flex-end', gap: 1 }}>
              <input
                ref={fileInputRef}
                type="file"
                onChange={handleFileChange}
                className="hidden"
                aria-hidden="true"
              />
              <Tooltip title="Attach file">
                <IconButton
                  onClick={handleFileAttachment}
                  sx={{ color: '#896161' }}
                  size="medium"
                >
                  <AttachFileIcon />
                </IconButton>
              </Tooltip>
              <TextField
                fullWidth
                multiline
                maxRows={4}
                value={inputValue}
                onChange={handleInputChange}
                onKeyDown={handleKeyDown}
                placeholder={language === 'EN' ? 'Type your question here...' : 'Sorunuzu buraya yazın...'}
                disabled={isLoading}
                variant="outlined"
                sx={{
                  '& .MuiOutlinedInput-root': {
                    backgroundColor: '#f8f6f6',
                    borderRadius: '12px',
                    '&:hover': {
                      backgroundColor: '#fff',
                    },
                    '&.Mui-focused': {
                      backgroundColor: '#fff',
                      '& fieldset': {
                        borderColor: '#d41111',
                      },
                    },
                  },
                }}
              />
              <Tooltip title="Send message">
                <span>
                  <IconButton
                    type="submit"
                    disabled={!inputValue.trim() || isLoading}
                    sx={{
                      backgroundColor: '#d41111',
                      color: 'white',
                      '&:hover': {
                        backgroundColor: '#b00e0e',
                      },
                      '&.Mui-disabled': {
                        backgroundColor: '#d4111150',
                        color: 'white',
                      },
                    }}
                  >
                    {isLoading ? <CircularProgress size={20} sx={{ color: 'white' }} /> : <SendIcon />}
                  </IconButton>
                </span>
              </Tooltip>
            </Box>
          </form>
          <p className="text-center text-[11px] text-[#896161]/60 mt-2">
            NEU Virtual Assistant can make mistakes. Verify important information with
            the Admissions Office.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ChatWindow;
