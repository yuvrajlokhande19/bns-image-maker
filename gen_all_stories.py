from pathlib import Path
import time
from generate_story_image import create_story_graphic

OUTPUT_DIR = Path("v2/output")

def main():
    post_images = sorted(list(OUTPUT_DIR.glob("BNS_post-*.jpg")))
    print(f"Found {len(post_images)} post images. Generating 9:16 Story graphics...")
    
    start = time.time()
    for i, post_path in enumerate(post_images, 1):
        # post-01 -> story-01
        story_filename = post_path.name.replace("BNS_post-", "BNS_story-")
        story_path = OUTPUT_DIR / story_filename
        create_story_graphic(post_path, story_path)
        if i % 20 == 0 or i == len(post_images):
            print(f"  Processed {i}/{len(post_images)}...")
            
    elapsed = time.time() - start
    print(f"Done! Generated {len(post_images)} 1080x1920 Story graphics in {elapsed:.1f}s.")

if __name__ == "__main__":
    main()
