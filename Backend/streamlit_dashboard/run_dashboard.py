"""
Dashboard Launcher Script

Run this script to start the Streamlit dashboard for chat analytics.
"""

import subprocess
import sys
import os


def main():
    """Launch the Streamlit dashboard"""
    dashboard_path = os.path.join(os.path.dirname(__file__), "dashboard.py")

    try:
        print("🚀 Starting Chat Analytics Dashboard...")
        print("📊 Dashboard will open in your browser")
        print("⏹️  Press Ctrl+C to stop the dashboard")
        print("-" * 50)

        # Run streamlit
        subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                dashboard_path,
                "--server.port",
                "8501",
                "--server.address",
                "localhost",
            ]
        )

    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure streamlit is installed: pip install streamlit")
        print("2. Check that all dependencies are installed")
        print("3. Ensure you're in the correct directory")


if __name__ == "__main__":
    main()
