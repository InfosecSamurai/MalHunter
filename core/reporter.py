import json
import logging
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

class ReportGenerator:
    def __init__(self, analysis_results):
        self.results = analysis_results
        self.logger = logging.getLogger(self.__class__.__name__)
        self.template_env = Environment(
            loader=FileSystemLoader(Path(__file__).parent / 'templates'),
            autoescape=True
        )
        
    def generate(self, output_path):
        """Generate analysis report in HTML format"""
        try:
            template = self.template_env.get_template('report_template.html')
            html = template.render(
                analysis=self.results,
                timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                settings=Settings
            )
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)
                
            self.logger.info(f"Report generated: {output_path}")
            
            # Also save JSON for programmatic use
            json_path = output_path.with_suffix('.json')
            with open(json_path, 'w') as f:
                json.dump(self.results, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Report generation failed: {e}")
            raise
