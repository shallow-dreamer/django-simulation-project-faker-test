from abc import ABC, abstractmethod
from typing import BinaryIO, Dict, Any, List
import numpy as np
import pandas as pd
from io import BytesIO
import logging

logger = logging.getLogger('apps')

class BaseFileProcessor(ABC):
    """
    文件处理器基类
    """
    @abstractmethod
    def process(self, file: BinaryIO) -> Dict[str, Any]:
        """处理文件内容"""
        pass

    @abstractmethod
    def validate(self, file: BinaryIO) -> bool:
        """验证文件格式"""
        pass

class TouchstoneProcessor(BaseFileProcessor):
    """
    Touchstone文件处理器
    """
    def process(self, file: BinaryIO) -> Dict[str, Any]:
        """
        处理Touchstone文件
        返回频率和S参数数据
        """
        try:
            content = file.read().decode('utf-8')
            lines = content.split('\n')
            
            # 解析文件头
            header = None
            for line in lines:
                if line.startswith('!'):
                    continue
                if line.startswith('#'):
                    header = line[1:].strip()
                    break
            
            if not header:
                raise ValueError("Invalid Touchstone file: no header found")
            
            # 解析数据
            data_lines = [line.strip() for line in lines if not line.startswith('!') and not line.startswith('#')]
            data = []
            for line in data_lines:
                if line:
                    data.append([float(x) for x in line.split()])
            
            data_array = np.array(data)
            frequency = data_array[:, 0]
            s_params = data_array[:, 1:]
            
            # 重构S参数
            s_matrix = {}
            for i in range(2):
                for j in range(2):
                    idx = (i * 2 + j) * 2
                    s_matrix[f's{i+1}{j+1}'] = {
                        'real': s_params[:, idx].tolist(),
                        'imag': s_params[:, idx + 1].tolist()
                    }
            
            return {
                'frequency': frequency.tolist(),
                'value': s_matrix
            }
            
        except Exception as e:
            logger.error(f"Failed to process Touchstone file: {e}")
            raise

    def validate(self, file: BinaryIO) -> bool:
        """
        验证Touchstone文件格式
        """
        try:
            content = file.read().decode('utf-8')
            file.seek(0)  # 重置文件指针
            
            lines = content.split('\n')
            
            # 检查文件头
            has_header = False
            for line in lines:
                if line.startswith('#'):
                    has_header = True
                    break
            
            if not has_header:
                return False
            
            # 检查数据格式
            data_lines = [line.strip() for line in lines if not line.startswith('!') and not line.startswith('#')]
            for line in data_lines:
                if line:
                    values = line.split()
                    if len(values) != 9:  # 频率 + 4个S参数(实部和虚部)
                        return False
                    try:
                        [float(x) for x in values]
                    except ValueError:
                        return False
            
            return True
        except Exception:
            return False

class ExcelProcessor(BaseFileProcessor):
    """
    Excel文件处理器
    """
    def process(self, file: BinaryIO) -> Dict[str, Any]:
        """
        处理Excel文件
        返回频率和S参数数据
        """
        try:
            df = pd.read_excel(file)
            
            # 验证必要的列
            required_columns = ['Frequency']
            s_param_columns = ['S11_R', 'S11_I', 'S12_R', 'S12_I',
                             'S21_R', 'S21_I', 'S22_R', 'S22_I']
            
            for col in required_columns + s_param_columns:
                if col not in df.columns:
                    raise ValueError(f"Missing required column: {col}")
            
            # 构建S参数矩阵
            s_matrix = {}
            for i in range(2):
                for j in range(2):
                    s_matrix[f's{i+1}{j+1}'] = {
                        'real': df[f'S{i+1}{j+1}_R'].tolist(),
                        'imag': df[f'S{i+1}{j+1}_I'].tolist()
                    }
            
            return {
                'frequency': df['Frequency'].tolist(),
                'value': s_matrix
            }
            
        except Exception as e:
            logger.error(f"Failed to process Excel file: {e}")
            raise

    def validate(self, file: BinaryIO) -> bool:
        """
        验证Excel文件格式
        """
        try:
            df = pd.read_excel(file)
            file.seek(0)
            
            # 检查必要的列
            required_columns = ['Frequency']
            s_param_columns = ['S11_R', 'S11_I', 'S12_R', 'S12_I',
                             'S21_R', 'S21_I', 'S22_R', 'S22_I']
            
            for col in required_columns + s_param_columns:
                if col not in df.columns:
                    return False
            
            # 检查数据类型
            try:
                df['Frequency'].astype(float)
                for col in s_param_columns:
                    df[col].astype(float)
            except ValueError:
                return False
            
            return True
        except Exception:
            return False 