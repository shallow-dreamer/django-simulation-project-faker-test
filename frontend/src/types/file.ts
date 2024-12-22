export interface FileCollection {
  id: number;
  name: string;
  description: string;
  created_at: string;
  updated_at: string;
}

export interface UploadedFile {
  id: number;
  file: string;
  name: string;
  file_type: string;
  collection: number | null;
  created_at: string;
  updated_at: string;
} 