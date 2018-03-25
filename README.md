# logoblur
A python script for batch blurring of image logos/objects using OpenCV.

To use:

```
python3 logoblur.py <image_folder> <logo_template.png>
```

Note, use with caution as original images will be overwritten.

## How does it work?

The script works via template matching. The algorithm looks for a region within the image that matches the given template. The crucial line is
```
result = cv2.matchTemplate(template, origImage, method)
```
where method is the least squared difference between the template and the original image. Note further that before the above API is applied, both the template and original images are converted to grayscale, before applying an edge detector which can help enhance the main features to be matched, i.e., these two lines here, for the template (the same process is applied to the actual image to be matched):
```
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
template = cv2.Canny(template, 50, 200)
```
Once the template has been matched, a mask is created from the matched area's rectangular region. This is used during the blending of the image-to-be-matched with a blurred copy. The mask will result in only the rectangular region becoming blurred. Note the mask itself is also blurred so that the effect of the final blended image, is to have a blurred region with feathered, rather than sharp edges.
