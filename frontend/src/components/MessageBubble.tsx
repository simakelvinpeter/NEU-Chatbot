import React from 'react';
import type { Message } from '../types';

interface MessageBubbleProps {
  message: Message;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.sender === 'user';
  const defaultBotAvatar = 'https://lh3.googleusercontent.com/aida-public/AB6AXuAGI0he52DtXffWJdVpjIdaUuTS-LYudDHB8OKoIFMWGXf-XJdmebDtfUX3TL0Y9sZTuo9wIOaOrpGyaGxqYzQETi1RHvy6tWO-nWfuzLwdJyuoiJVZVsxQdvY_u9epdCyIq7HOpzJsW9Ue6KV6hb-sExb4ZRpuO7gQJSW43Km1k-gpffnajdT3tSe-SgP_2_TcFaYB5AGft5TIw1OxEiI3YPgcrhF-GqNDwvvgLSLrco5tTK46D7xABjMNkVtD_73vmNRh7EMUw2Qg';
  const defaultUserAvatar = 'https://lh3.googleusercontent.com/aida-public/AB6AXuCyjMwT6G4Cw52AvAxkECuMteFCN0853yMnt-DrrJL6bbDDbl8G3uuQVhJQULWL-kohtjdA64eK_hAhp27zRc1n_tw4eCYiW-QKWzs1gxuj4gScoUN1dtqwTU_WfKYSdE1FBLEeXOkAXQ1zK0z-V_OmNoyHW_g6FcnjkSMU5pb5vVF3fHdqz6CInjk413nQX-HwN4TtXNAwVow9MZax8kqbDnxWU7n1gN5TZei_uvQbCYOghqgG8jl138mZfGo21X_gBB2BKVdSTVN4';

  if (isUser) {
    return (
      <div className="flex items-end gap-3 max-w-[85%] ml-auto justify-end">
        <div className="flex flex-col gap-1 items-end">
          <span className="text-[#896161] text-xs font-medium mr-1">You</span>
          <div className="text-base font-normal leading-relaxed rounded-2xl rounded-br-none px-5 py-3 bg-primary text-white shadow-md">
            <p>{message.content}</p>
          </div>
        </div>
        <div
          className="bg-center bg-no-repeat aspect-square bg-cover rounded-full w-10 h-10 shrink-0 shadow-sm"
          style={{ backgroundImage: `url("${message.avatar || defaultUserAvatar}")` }}
          role="img"
          aria-label="User avatar"
        />
      </div>
    );
  }

  return (
    <div className="flex items-end gap-3 max-w-[85%]">
      <div
        className="bg-center bg-no-repeat aspect-square bg-cover rounded-full w-10 h-10 shrink-0 shadow-sm"
        style={{ backgroundImage: `url("${message.avatar || defaultBotAvatar}")` }}
        role="img"
        aria-label="NEU Bot avatar"
      />
      <div className="flex flex-col gap-1 items-start">
        <span className="text-[#896161] text-xs font-medium ml-1">NEU Bot</span>
        <div 
          className="text-base font-normal leading-relaxed rounded-2xl rounded-bl-none px-5 py-3 bg-white text-[#181111] shadow-sm border border-[#f0f0f0]"
          dangerouslySetInnerHTML={{ __html: message.content }}
        />
      </div>
    </div>
  );
};

export default MessageBubble;
