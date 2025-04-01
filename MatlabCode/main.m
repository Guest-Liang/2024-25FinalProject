clear; close all; clc;
%% Group 1

original1 = imread('../../BBC6521-Final-Report-LaTeX/figures/4.png');
encrypted1 = imread('../../BBC6521-Final-Report-LaTeX/figures/4_ImageKey.png');

% 灰度图
if size(original1, 3) == 3
    original1_gray = rgb2gray(original1);
else
    original1_gray = original1;
end
if size(encrypted1, 3) == 3
    encrypted1_gray = rgb2gray(encrypted1);
else
    encrypted1_gray = encrypted1;
end

% PSNR与SSIM
psnr1 = psnr(encrypted1_gray, original1_gray);
ssim1 = ssim(encrypted1_gray, original1_gray);
fprintf('Group 1 - PSNR: %.2f dB, SSIM: %.4f\n', psnr1, ssim1);

% 噪声图像-绝对差异
noise1 = imabsdiff(original1_gray, encrypted1_gray);

% Figure1: 原始图像与加密图像
figure('Name', 'Group 1 - Original vs Encrypted', 'NumberTitle', 'off');
subplot(1,2,1), imshow(original1), title('Group 1: Original (4.png)');
subplot(1,2,2), imshow(encrypted1), title('Group 1: Encrypted (4\_ImageKey.png)');

% Figure 2: 噪声图像
figure('Name', 'Group 1 - Noise and Histogram', 'NumberTitle', 'off');
imshow(noise1, []), title('Group 1: Noise Image (diff)');

% Figure 3: 频谱分析
F_original1 = fftshift(fft2(original1_gray));
spectrum_original1 = log(1 + abs(F_original1));
F_encrypted1 = fftshift(fft2(encrypted1_gray));
spectrum_encrypted1 = log(1 + abs(F_encrypted1));
figure('Name', 'Group 1 - Frequency Spectrum', 'NumberTitle', 'off');
subplot(1,2,1), imshow(mat2gray(spectrum_original1)), title('Group 1: Frequency Spectrum (Original)');
subplot(1,2,2), imshow(mat2gray(spectrum_encrypted1)), title('Group 1: Frequency Spectrum (Encrypted)');

%% Group 2 Analysis

original2 = imread('../../BBC6521-Final-Report-LaTeX/figures/3.png');
encrypted2 = imread('../../BBC6521-Final-Report-LaTeX/figures/3_ImageKey.png');

if size(original2, 3) == 3
    original2_gray = rgb2gray(original2);
else
    original2_gray = original2;
end
if size(encrypted2, 3) == 3
    encrypted2_gray = rgb2gray(encrypted2);
else
    encrypted2_gray = encrypted2;
end

psnr2 = psnr(encrypted2_gray, original2_gray);
ssim2 = ssim(encrypted2_gray, original2_gray);
fprintf('Group 2 - PSNR: %.2f dB, SSIM: %.4f\n', psnr2, ssim2);

noise2 = imabsdiff(original2_gray, encrypted2_gray);

figure('Name', 'Group 2 - Original vs Encrypted', 'NumberTitle', 'off');
subplot(1,2,1), imshow(original2), title('Group 2: Original (3.png)');
subplot(1,2,2), imshow(encrypted2), title('Group 2: Encrypted (3\_ImageKey.png)');

figure('Name', 'Group 2 - Noise and Histogram', 'NumberTitle', 'off');
imshow(noise2, []), title('Group 2: Noise Image (diff)');

F_original2 = fftshift(fft2(original2_gray));
spectrum_original2 = log(1 + abs(F_original2));
F_encrypted2 = fftshift(fft2(encrypted2_gray));
spectrum_encrypted2 = log(1 + abs(F_encrypted2));
figure('Name', 'Group 2 - Frequency Spectrum', 'NumberTitle', 'off');
subplot(1,2,1), imshow(mat2gray(spectrum_original2)), title('Group 2: Frequency Spectrum (Original)');
subplot(1,2,2), imshow(mat2gray(spectrum_encrypted2)), title('Group 2: Frequency Spectrum (Encrypted)');
