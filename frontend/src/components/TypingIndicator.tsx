import React from 'react';

const TypingIndicator: React.FC = () => {
  return (
    <div className="typing-indicator-container" style={{
      display: 'flex',
      justifyContent: 'flex-start',
      marginBottom: '16px',
      animation: 'fadeIn 0.3s ease-in'
    }}>
      <div style={{
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        borderRadius: '18px',
        padding: '12px 16px',
        maxWidth: '80px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
      }}>
        <div className="typing-dots" style={{
          display: 'flex',
          gap: '4px',
          alignItems: 'center'
        }}>
          <span className="dot" style={{
            width: '8px',
            height: '8px',
            backgroundColor: 'white',
            borderRadius: '50%',
            animation: 'typing 1.4s infinite',
            animationDelay: '0s'
          }}></span>
          <span className="dot" style={{
            width: '8px',
            height: '8px',
            backgroundColor: 'white',
            borderRadius: '50%',
            animation: 'typing 1.4s infinite',
            animationDelay: '0.2s'
          }}></span>
          <span className="dot" style={{
            width: '8px',
            height: '8px',
            backgroundColor: 'white',
            borderRadius: '50%',
            animation: 'typing 1.4s infinite',
            animationDelay: '0.4s'
          }}></span>
        </div>
      </div>
      <style>
        {`
          @keyframes typing {
            0%, 60%, 100% {
              transform: translateY(0);
              opacity: 0.7;
            }
            30% {
              transform: translateY(-10px);
              opacity: 1;
            }
          }
          
          @keyframes fadeIn {
            from {
              opacity: 0;
              transform: translateY(10px);
            }
            to {
              opacity: 1;
              transform: translateY(0);
            }
          }
        `}
      </style>
    </div>
  );
};

export default TypingIndicator;
