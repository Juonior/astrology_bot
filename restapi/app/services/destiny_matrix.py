from datetime import datetime, time, date
from fastapi import HTTPException
from typing import Dict, List
from schemas.responses import DestinyMatrixResponse

class DestinyMatrixService:
    def __init__(self):
        self.interpretations = {
            1: "Характер, воля",
            2: "Энергетика, эмоции",
            3: "Интерес к наукам",
            4: "Здоровье",
            5: "Логика, интуиция",
            6: "Склонность к труду",
            7: "Удача",
            8: "Чувство долга",
            9: "Память, интеллект"
        }

    async def calculate_matrix(self, birth_date: date) -> DestinyMatrixResponse:
        try:
            # Конвертируем date в datetime с временем 00:00
            birth_datetime = datetime.combine(birth_date, time.min)
            
            date_str = birth_datetime.strftime("%d%m%Y")
            digits = self._calculate_digits(date_str)
            
            destiny_number = self._sum_digits(sum(digits))
            personality_number = self._sum_digits(sum(int(d) for d in str(birth_date.day)))
            life_path_number = self._sum_digits(
                self._sum_digits(birth_date.day) + 
                self._sum_digits(birth_date.month) + 
                self._sum_digits(birth_date.year)
            )

            matrix = self._build_matrix(digits)
            
            return DestinyMatrixResponse(
                birth_date=birth_date.isoformat(),
                energy_centers=self._calculate_energy_centers(matrix),
                money_line=[matrix[i][i] for i in range(3)],
                family_line=matrix[0],
                health_line=matrix[1],
                talents_line=matrix[2],
                destiny_number=destiny_number,
                personality_number=personality_number,
                life_path_number=life_path_number,
                matrix=matrix,
                interpretation=self._get_interpretation(matrix)
            )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Ошибка расчета матрицы: {str(e)}"
            )

    def _calculate_digits(self, date_str: str) -> List[int]:
        return [int(c) for c in date_str if c.isdigit()]

    def _sum_digits(self, number: int) -> int:
        while number > 9 and number not in [11, 22]:  # Сохраняем мастер-числа
            number = sum(int(d) for d in str(number))
        return number

    def _build_matrix(self, digits: List[int]) -> List[List[int]]:
        matrix = [[0]*3 for _ in range(3)]
        for digit in digits:
            if 1 <= digit <= 9:
                row = (digit - 1) // 3
                col = (digit - 1) % 3
                matrix[row][col] += 1
        return matrix

    def _calculate_energy_centers(self, matrix: List[List[int]]) -> Dict[str, int]:
        return {
            "head": sum(matrix[0]),
            "heart": sum(matrix[1]),
            "root": sum(matrix[2])
        }

    def _get_interpretation(self, matrix: List[List[int]]) -> str:
        interpretation = []
        for i in range(3):
            for j in range(3):
                num = i*3 + j + 1
                count = matrix[i][j]
                if count > 0:
                    interpretation.append(
                        f"{num} ({self.interpretations[num]}): {count}"
                    )
        return "; ".join(interpretation)