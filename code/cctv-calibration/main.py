import numpy as np
import torch
from PIL import Image

from unidepth.models import UniDepthV1, UniDepthV2
from unidepth.utils import colorize, image_grid


def resize_image(image, target_size):
    return np.array(Image.fromarray(image).resize(target_size[::-1], Image.BILINEAR))

def demo(model):
    rgb = np.array(Image.open("assets/demo/10m_2.jpg"))
    depth_gt = np.array(Image.open("assets/demo/depth.png")).astype(float) / 1000.0

    # Resize depth_gt to match the RGB image size
    depth_gt_resized = resize_image(depth_gt, rgb.shape[:2])

    rgb_torch = torch.from_numpy(rgb).permute(2, 0, 1).unsqueeze(0).float() / 255.0
    intrinsics_torch = torch.from_numpy(np.load("assets/demo/intrinsics.npy"))

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    rgb_torch = rgb_torch.to(device)
    intrinsics_torch = intrinsics_torch.to(device)

    # predict
    predictions = model.infer(rgb_torch, intrinsics_torch)

    # get GT and pred
    depth_pred = predictions["depth"].squeeze().cpu().numpy()

    # compute error, you have zero divison where depth_gt == 0.0
    depth_arel = np.abs(depth_gt_resized - depth_pred) / depth_gt_resized
    depth_arel[depth_gt_resized == 0.0] = 0.0

    # colorize
    depth_pred_col = colorize(depth_pred, vmin=0.01, vmax=10.0, cmap="magma_r")
    depth_gt_col = colorize(depth_gt_resized, vmin=0.01, vmax=10.0, cmap="magma_r")
    depth_error_col = colorize(depth_arel, vmin=0.0, vmax=0.2, cmap="coolwarm")

    # save image with pred and error
    artifact = image_grid([rgb, depth_gt_col, depth_pred_col, depth_error_col], 2, 2)
    Image.fromarray(artifact).save("assets/demo/output.png")

    print("Available predictions:", list(predictions.keys()))
    print(f"ARel: {depth_arel[depth_gt_resized > 0].mean() * 100:.2f}%")

    # 특정 좌표(800, 600)의 깊이 출력
    x, y = 800, 600
    depth_at_point = depth_pred[y, x]
    print(f"Depth at ({x}, {y}): {depth_at_point:.4f} meters")


if __name__ == "__main__":
    print("Torch version:", torch.__version__)
    name = "unidepth-v2-vitl14"
    model = UniDepthV2.from_pretrained(f"lpiccinelli/{name}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    demo(model)

