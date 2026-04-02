import os

import pdfkit

from config import env_config
from core.utils import constant_variable


class HTMLTOPDFSERVICE:

    def html_to_pdf(self, file_path: str, render_html: str):
        """
        Converts HTML content to a PDF file and saves it to the specified path.

        Args:
            file_path (str): The file path where the PDF will be saved.
            render_html: The HTML content to be converted to PDF.

        Returns:
            str: The file path of the generated PDF if successful, None otherwise.
        """
        try:
            margin = "0in"
            options = {
                "page-size": "A4",
                "margin-top": margin,
                "margin-right": margin,
                "margin-bottom": margin,
                "margin-left": margin,
                "encoding": "UTF-8",
                "disable-javascript": constant_variable.STATUS_TRUE,  # Disable JS if not needed
            }
            if not os.path.exists(file_path):
                os.makedirs(file_path)

            # Convert HTML to PDF
            config = pdfkit.configuration(wkhtmltopdf=env_config.WKHTMLOPDF_PATH)
            pdfkit.from_string(
                render_html, file_path, configuration=config, options=options
            )
            return file_path
        except Exception:
            return constant_variable.STATUS_NULL
