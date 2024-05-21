from crewai_tools import BaseTool
import csv
import io
from typing import Dict, Any

class CSVCreationTool(BaseTool):
    """Compiles data into a CSV format."""
    name: str = "CSV Creation Tool"
    description: str = "Compiles data into a CSV format."

    def _run(self, data: Dict[str, Any]) -> str:
        try:
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Ensure headers and rows exist in data
            headers = data.get('headers')
            rows = data.get('rows')

            if not headers or not rows:
                raise ValueError("Data must contain 'headers' and 'rows' keys with non-empty values.")

            writer.writerow(headers)
            writer.writerows(rows)
            
            return output.getvalue()
        except Exception as e:
            return f"Error creating CSV: {str(e)}"
