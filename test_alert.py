"""Send one fake alert so you can check your phone gets it."""
from datetime import datetime, timedelta, timezone

import ats
import radar

job = ats.Job("greenhouse", "test", "Job Radar test", "0", "AI Engineer (test alert)",
              "Remote, US", "https://github.com", datetime.now(timezone.utc) - timedelta(minutes=4))
radar.notify(job, "AI Engineer resume", ["this is a test"], "Sponsors (12 tech H-1B filings since FY2025)", 4)
print("test alert sent")
