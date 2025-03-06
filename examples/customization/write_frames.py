import cv2
import os
import argparse
from pathlib import Path

def extract_frames(video_path, output_folder, frame_prefix = None):
    if frame_prefix is None:
        frame_prefix = Path(video_path).stem

    os.makedirs(output_folder, exist_ok = True)
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print(f"Error: Could not open video {video_path}")
        return 0
    
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps if fps > 0 else 0
    
    print(f"Processing '{video_path}':")
    print(f"  - FPS: {fps:.2f}")
    print(f"  - Total frames: {frame_count}")
    print(f"  - Duration: {duration:.2f} seconds")
    
    count = 0
    success = True

    while success:

        success, frame = video.read()
        
        if success:
            # Save the frame as JPEG
            frame_filename = f"{frame_prefix}_frame_{count:06d}.jpg"
            frame_path = os.path.join(output_folder, frame_filename)
            cv2.imwrite(frame_path, frame)
            count += 1
            
            if count % 100 == 0:
                print(f"  - Extracted {count} frames so far...")
    
    video.release()
    
    print(f"  - Completed: {count} frames extracted to {output_folder}")
    return count

def process_vids(input_folder, output_folder, extensions=None):
    if extensions is None:
        extensions = ['.mp4', '.avi', '.mkv', '.mov']
    
    # Convert extensions to lowercase for case-insensitive matching
    extensions = [ext.lower() for ext in extensions]
    
    os.makedirs(output_folder, exist_ok=True)
    
    video_files = []
    for file in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file)
        if os.path.isfile(file_path) and os.path.splitext(file)[1].lower() in extensions:
            video_files.append(file_path)
    
    if not video_files:
        print(f"No video files with extensions {extensions} found in {input_folder}")
        return 0
    
    print(f"Found {len(video_files)} video files to process.")
    
    total_videos = 0
    total_frames = 0
    
    for video_path in video_files:
        # Use video filename as prefix for frame filenames
        video_name = Path(video_path).stem
        
        frames = extract_frames(video_path, output_folder, frame_prefix=video_name)
        
        if frames > 0:
            total_videos += 1
            total_frames += frames
    
    print(f"\nSummary:")
    print(f"  - Total videos processed: {total_videos}")
    print(f"  - Total frames extracted: {total_frames}")
    print(f"  - Output directory: {output_folder}")
    
    return total_videos

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Extract frames from videos in a folder')
    
    parser.add_argument('input_folder', type=str, help='Folder containing video files')
    parser.add_argument('output_folder', type=str, help='Folder to save extracted frames')
    parser.add_argument('--extensions', type=str, nargs='+', 
                        default=['.mp4', '.avi', '.mkv', '.mov'],
                        help='Video file extensions to process (default: .mp4 .avi .mkv .mov)')
    
    args = parser.parse_args()
    
    process_vids(args.input_folder, args.output_folder, args.extensions)