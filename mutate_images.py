from pathlib import Path
import typer
import subprocess

def find_image_files(path: str):
    """Find all images in the given directory and its subdirectories."""
    frames = Path(path)
    return (
        list(frames.rglob("*.png"))
        + list(frames.rglob("*.jpg"))
        + list(frames.rglob("*.jpeg"))
        + list(frames.rglob("*.bmp"))
        + list(frames.rglob("*.tif"))
        + list(frames.rglob("*.tiff"))
        + list(frames.rglob("*.gif"))
    )

app = typer.Typer()

# %%


@app.command()
def mutate(
    prompt: str = "fantasy character art portrait | colored ink | tronie | defined eyes",
    init_images: Path = "",
):
    """Mutate images in the given directory."""
    print(f"Initial image: {init_images}")
    print(f"Prompt: {prompt}")
    print("Mutating images...")
    for image in find_image_files(init_images):
        print(f"Mutating {image}")
        ## TODO this reloads clip for each subprocess, better to import and run all
        res = subprocess.run(
            [
                "python",
                # "aesthetic_sample.py",
                "sample.py",

                "--model_path", "models/ongo.pt",
                "--bert_path", "models/bert.pt",
                "--kl_path", "models/kl-f8.pt",
                "--batch_size", "20",
                "--num_batches", "1",
                "--negative",
                "low quality, bad art, blurry, distorted, deformed face, marred, skin blemishes, gross face, crossed eyes, crazed eyes",
                "--steps", "20",
                "--guidance_scale", "12",
                "--text", prompt,
                "--init_image", image,
                "--skip_timesteps", "8",
                # "--prompt_file", "",
                # "--aesthetic_weight", "0.0",
                # "--output_dir", "output_mutated",
            ]
        )
    print("Done.")


if __name__ == "__main__":
    app()