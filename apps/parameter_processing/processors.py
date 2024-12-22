import numpy as np
from typing import Dict, Any, List
from .exceptions import ProcessingError

class SParameterProcessor:
    """
    S参数处理器
    """
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.frequency = np.array(data.get('frequency', []))
        self.s_parameters = self._parse_s_parameters(data.get('value', {}))
    
    def _parse_s_parameters(self, value: Dict) -> Dict[str, np.ndarray]:
        """
        解析S参数数据
        """
        result = {}
        for key, val in value.items():
            if isinstance(val, dict) and 'real' in val and 'imag' in val:
                result[key] = np.array(val['real']) + 1j * np.array(val['imag'])
        return result
    
    def apply_frequency_filter(self, min_freq: float, max_freq: float) -> Dict:
        """
        应用频率过滤
        """
        mask = (self.frequency >= min_freq) & (self.frequency <= max_freq)
        filtered_data = {
            'frequency': self.frequency[mask].tolist(),
            'value': {}
        }
        
        for key, val in self.s_parameters.items():
            filtered_val = val[mask]
            filtered_data['value'][key] = {
                'real': filtered_val.real.tolist(),
                'imag': filtered_val.imag.tolist()
            }
        
        return filtered_data
    
    def calculate_impedance(self) -> Dict[str, List[float]]:
        """
        计算阻抗
        """
        z0 = 50.0  # 特征阻抗
        try:
            s11 = self.s_parameters.get('s11', np.array([]))
            z_in = z0 * (1 + s11) / (1 - s11)
            return {
                'magnitude': np.abs(z_in).tolist(),
                'phase': np.angle(z_in, deg=True).tolist()
            }
        except Exception as e:
            raise ProcessingError(f"阻抗计算失败: {str(e)}") 