import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, File, X } from 'lucide-react';
import useCaseStore from '../store/useCaseStore';
import { agentAPI } from '../api';

const FileDropzone = () => {
  const { uploadedFiles, addUploadedFile, removeUploadedFile } = useCaseStore();

  const onDrop = useCallback(async (acceptedFiles) => {
    for (const file of acceptedFiles) {
      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await agentAPI.uploadFile(formData);
        addUploadedFile({
          id: response.data.file_id,
          name: file.name,
          size: file.size,
          type: file.type,
          extractedText: response.data.extracted_text
        });
      } catch (error) {
        console.error('Error uploading file:', error);
      }
    }
  }, [addUploadedFile]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/*': ['.png', '.jpg', '.jpeg'],
      'text/*': ['.txt', '.doc', '.docx']
    }
  });

  return (
    <div className="p-4 border-b border-gray-200">
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-xl p-4 text-center cursor-pointer transition-colors
          ${isDragActive ? 'border-gray-400 bg-gray-50' : 'border-gray-300 hover:border-gray-400'}
        `}
      >
        <input {...getInputProps()} />
        <Upload size={24} className="mx-auto mb-2 text-gray-400" />
        <p className="text-sm text-gray-600">
          {isDragActive ? 'Drop files here...' : 'Drop files or click to upload'}
        </p>
        <p className="text-xs text-gray-500 mt-1">PDF, images, text files</p>
      </div>

      {uploadedFiles.length > 0 && (
        <div className="mt-3 space-y-2">
          {uploadedFiles.map((file) => (
            <div key={file.id} className="flex items-center gap-2 p-2 bg-gray-50 rounded-lg">
              <File size={16} className="text-gray-400" />
              <span className="text-sm text-gray-700 flex-1 truncate">{file.name}</span>
              <button
                onClick={() => removeUploadedFile(file.id)}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <X size={14} />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default FileDropzone;