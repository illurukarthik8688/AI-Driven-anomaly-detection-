import os
import sys

# Threshold in seconds (you can change this later)
THRESHOLD = 12

# Get build time from GitHub environment
build_time = float(os.getenv("BUILD_TIME", 0))

print(f"Received Build Time: {build_time} seconds")

if build_time > THRESHOLD:
    print("⚠️ Anomaly Detected: Build time exceeded threshold!")
    sys.exit(1)   # This will FAIL the pipeline
else:   
    print("✅ Build time is normal.")
