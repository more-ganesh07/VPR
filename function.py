from Config.config import *

def redirect_button(url: str, text: str= None, color="#FD504D"):
    st.markdown(
    f"""
    <a href="{url}" target="_self">
        <div style="
            display: inline-block;
            padding: 0.5em 1em;
            color: #FFFFFF;
            background-color: {color};
            border-radius: 3px;
            text-decoration: none;">
            {text}
        </div>
    </a>
    """,
    unsafe_allow_html=True
    )

def open_url(url):
    """
    Open a URL in a new browser tab when clicked in a user interface.

    Parameters:
        url (str): The URL to be opened in a new browser tab when clicked.

    Usage:
        - This function can be used in a web application or user interface to create a clickable link.
        - When the link is clicked by the user, it opens the provided URL in a new browser tab.
    """
    js = f"window.open('{url}')"  # JavaScript to open URL in a new tab
    html = '<img src onerror="{}">'.format(js)  # Trick to execute JavaScript
    st.write(html, unsafe_allow_html=True)



def get_product_link(request_product_in):
    """
    Fetches product links from an SQLite database using the product name and company and returns the links.

    Parameters:
        request_product (str): The name of the product and, optionally, the company (e.g., "Apple Watch Series 8").

    Returns:
        list of str: A list of product links matching the provided product name and company, if found in the database.
    """
    try:
        print("befre request", request_product_in)
        request_product = get_mapping(request_product_in)
        print("after mapping",request_product)

        # Create a connection to the SQLite database
        conn = sqlite3.connect(os.path.join(path,"my_database.db"))
        cursor = conn.cursor()
        
        if request_product == "CASIO Vintage (A-158WA-1Q) Digital Watch":
            product_links = [("https://www.flipkart.com/casio-a-158wa-1df-vintage-a-158wa-1q-digital-watch-men-women/p/itmf3zhdga85ghju",)]
        else:
            # Define a SQL statement to retrieve product links based on the concatenated company and product name
            statement = "SELECT link FROM watch WHERE company || ' ' || product = ?"
        
            # Execute the SQL statement with the provided 'request_product'
            cursor.execute(statement, (request_product,))
            
            # Fetch the product links from the database
            product_links = cursor.fetchall()
        # print("Fetched Result:",product_links)
        print(product_links)

        # Return the list of product links
        return product_links
    except Exception as e:
        # Return the exception object in case of an error
        return e
    finally:
        # Close the database connection in the 'finally' block to ensure it's always closed
        conn.close()


def get_yolo_output(uploaded_image):
    """
    Detect objects in an uploaded image using YOLOv3 model.

    Parameters:
        uploaded_image (str): The filename of the image to process.
    """
    # Create a CustomObjectDetection instance
    detector = CustomObjectDetection()

    # Set the model type to YOLOv3
    detector.setModelTypeAsYOLOv3()

    # Set the path to the YOLOv3 model and configuration files
    detector.setModelPath(os.path.join(path, "Yolo-model\models\yolov3_SplitData_last_vijay.pt"))
    detector.setJsonPath(os.path.join(path, "Yolo-model\json\SplitData_yolov3_detection_config_vijay.json"))

    # Load the YOLOv3 model
    detector.loadModel()

    # Perform object detection on the uploaded image
    detections = detector.detectObjectsFromImage(
        input_image=os.path.join(path, 'input', uploaded_image),
        output_image_path=os.path.join(path, "Yolo_Output_image", f"{uploaded_image}"),
    )

    return detections
    
def get_custom_bouding_box(uploaded_image, yolo_output_in, frame_size, uploaded_image_name):
    bo_image = Image.open(uploaded_image)
    draw = ImageDraw.Draw(bo_image)

    # Load a larger font for labels
    font_path = os.path.join(path, r"Config\aloevera-font\Aloevera-OVoWO.ttf")
    font_size = 22
    font = ImageFont.truetype(font_path, font_size)

    # Defining colors
    if len(yolo_output_in) > 1:
        box_colors = {
            "Aapple Watch Series 8": "green",
            "Apple Watch Series 8": "green",
            "One PLus - Band": "purple",
            "OnePlus Band":"purple",
            "CASIO Vintage ( A-158WA-1Q ) Digital Watch": "yellow",
            "Fastrack Minimalists Analog Watch": "green",
            "Fireboltt Ninja Calling Pro Plus": "green",
            "Fossil Briggs Analog - CH2927I": "yellow",
            "Casio G-Shock (( DW-5600BB-1DR ) Analog Watch)": "yellow",
            "Noise Evolve 3": "green",
            "Samsung Watch 4": "green",
            "default":"white"
        }
        print("yolo output before interation",yolo_output_in)
        for eachObject in yolo_output_in:
            yolo_output_in = get_mapping(yolo_output_in)
            if eachObject is not None:
                label = eachObject['name']
                box_points = eachObject['box_points']
                box_color = box_colors.get(label, box_colors['default'])
                box_color_rgb = ImageColor.getrgb(box_color) if isinstance(box_color, str) else box_color
                x1, y1, x2, y2 = box_points
                draw.rectangle([x1, y1, x2, y2], outline=box_color_rgb, width=10)
                
                label_width, label_height = draw.textsize(label, font=font)
                draw.rectangle([x1, y1 - label_height, x1 + label_width, y1], fill=box_color_rgb)
                draw.text((x1, y1 - label_height), label, fill="white", font=font)
            else:
                pass

    elif len(yolo_output_in) == 1:
        box_colors = {'default': 'yellow'}

    
        print("yolo output before interation",yolo_output_in)
        for eachObject in yolo_output_in:
            if eachObject is not None:
                label = eachObject['name']
                box_points = eachObject['box_points']
                box_color = box_colors.get(label, box_colors['default'])
                box_color_rgb = ImageColor.getrgb(box_color) if isinstance(box_color, str) else box_color
                x1, y1, x2, y2 = box_points
                draw.rectangle([x1, y1, x2, y2], outline=box_color_rgb, width=10)
                
                label_width, label_height = draw.textsize(label, font=font)
                draw.rectangle([x1, y1 - label_height, x1 + label_width, y1], fill=box_color_rgb)
                draw.text((x1, y1 - label_height), label, fill="white", font=font)
            else:
                pass

    bo_resized_image = bo_image.resize(frame_size, Image.ANTIALIAS)
    bo_resized_image.save(os.path.join(path,"Output_image",f"op{uploaded_image_name}"))
    bo_resized_image_path = os.path.join(path,"Output_image",f"op{uploaded_image_name}")
    return bo_resized_image, bo_resized_image_path


def remove_files_in_folder(folder_path):
    try:
        # List all files in the folder
        files = os.listdir(folder_path)

        # Loop through the files and remove each one
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            
            # Check if the path is a file (not a directory)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Removed: {file_path}")
            else:
                print(f"Skipped: {file_path} (not a file)")

        # print(f"All files in {folder_path} have been removed.")
    except Exception as e:
        pass

def get_mapping(input):
    print("inside Mapping")
    if input == "Aapple Watch Series 8":
        return "Apple Watch Series 8"
    elif input == "Casio Vintage ( A-158WA-1Q ) Digital Watch 2":
        return "CASIO Vintage (A-158WA-1Q) Digital Watch"
    elif input == "One PLus - Band":
        return "OnePlus Band"
    elif input == "Fire-Boltt Ninja Calling Pro Plus":
        return "Fireboltt Ninja Calling Pro Plus"
    elif input=="Noise Evolve 3":
        return "Noise Evolve 3"
    elif input=="Fastrack Minimalists Analog Watch":
        return "Fastrack Minimalists Analog Watch"
    else:
        return None
