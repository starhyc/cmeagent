import subprocess
import os

class PandocConverter:
    def __init__(self):
        pass

    def convert_to_pdf(self, markdown_path: str, pdf_path: str) -> bool:
        try:
            subprocess.run([
                'pandoc',
                markdown_path,
                '-o', pdf_path,
                '--pdf-engine=xelatex',
                '-V', 'geometry:margin=1in'
            ], check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            raise Exception(f"PDF conversion failed: {e.stderr.decode()}")
        except FileNotFoundError:
            raise Exception("Pandoc not installed. Install with: apt-get install pandoc texlive-xetex")
