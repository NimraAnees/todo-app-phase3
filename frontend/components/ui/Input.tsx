import React, { useState } from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helpText?: string;
  showPasswordToggle?: boolean;
  onPasswordToggle?: () => void;
  icon?: React.ReactNode;
}

const Input: React.FC<InputProps> = ({
  label,
  error,
  helpText,
  showPasswordToggle = false,
  onPasswordToggle,
  icon,
  className = '',
  type,
  ...props
}) => {
  const [showPassword, setShowPassword] = useState(false);
  const isPasswordType = type === 'password';
  const showToggle = isPasswordType && showPasswordToggle;

  const baseClasses = 'flex w-full rounded-md border bg-onyx-800 px-3 py-3 text-sm text-onyx-50 ring-offset-onyx-900 file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-onyx-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50';

  const errorClass = error ? 'border-rose-500 focus-visible:ring-rose-500' : 'border-onyx-600';

  const inputClasses = `${baseClasses} ${errorClass} ${className}`;

  const handlePasswordToggle = () => {
    if (onPasswordToggle) {
      onPasswordToggle();
    } else {
      setShowPassword(!showPassword);
    }
  };

  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-onyx-300 mb-1">
          {label}
        </label>
      )}
      <div className="relative">
        <input
          type={isPasswordType && (showPassword || (onPasswordToggle ? showPasswordToggle : false)) ? 'text' : type}
          className={`${inputClasses} ${icon ? 'pl-10' : ''} pr-10`}
          {...props}
        />
        {icon && (
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <div className="text-onyx-400">
              {icon}
            </div>
          </div>
        )}
        {showToggle && (
          <button
            type="button"
            onClick={handlePasswordToggle}
            className="absolute inset-y-0 right-0 pr-3 flex items-center text-onyx-400 hover:text-onyx-300"
          >
            {isPasswordType && (showPassword || (onPasswordToggle ? showPasswordToggle : false)) ? (
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-1.563 3.029m-9.344 0A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a10.025 10.025 0 011.563-3.029m-1.036 0a13.998 13.998 0 017.532-7.532"></path>
              </svg>
            ) : (
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
              </svg>
            )}
          </button>
        )}
      </div>
      {error && (
        <p className="mt-1 text-sm text-rose-400">{error}</p>
      )}
      {helpText && !error && (
        <p className="mt-1 text-sm text-onyx-400">{helpText}</p>
      )}
    </div>
  );
};

export default Input;
