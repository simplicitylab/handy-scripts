## imageq

Script that displays images that don't meet a minimum resolution requirement

**Usage**:

```bash
python imageq.py image_directory minimum_resolution
```

**Example**:

Filter images in the header_images that are smaller than 1024x200

```bash
python imageq.py header_images 1024x200
```

**Example output**

```
Images that does not meet the minimum resolution requirements:

* 1024x150.png [1024x150]
* 350x150.png [350x150]
* 640x480.png [640x480]
```
