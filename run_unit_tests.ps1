## Runs tests and generates coverage report
## Use -report to automatically open html report in default browser

param(
  [switch]$report # Defines a flag for opening html report
)

coverage run -m unittest discover -s tests\
coverage report
coverage html

# Gets path to html report
$coverageReportPath = Join-Path (Get-Location) "htmlcov\index.html"

if ($report) {
  # Check if the index.html file exists
  if (Test-Path $coverageReportPath) {
    # Open the index.html file in the default web browser
    Start-Process $coverageReportPath
  } else {
    Write-Host "Coverage report not found."
  }
}