# Import required modules and functions from custom modules
from Config.config import *
from Functions.functions import *

# Define the main function
def main():
    # Create the Streamlit application layout
    with st.container():
        col_imag, col_title = st.columns([1, 3])
        col_imag.image(cdac_logo, width=100, clamp=True)  
        col_title.subheader('Visual Product Recognition')

    # Define the frame size for processed images
    frame_size = (300, 300)

    # Create columns for image upload and processing
    col1, col2 = st.columns([1, 3])
    with col1:
        try:
            uploaded_image = st.file_uploader("", type=["jpg", "png", "jpeg"])
        except:
            col2.write("Incorrect File..!")    

    with col2:
        if uploaded_image is not None:
            col2Image1, col2Image2 = col2.columns([1, 1])
            image = Image.open(uploaded_image)
            upload_image_path = os.path.join(path, "input", uploaded_image.name)
            # Save the uploaded image
            image.save(upload_image_path)
            
            resized_image = image.resize(frame_size, Image.ANTIALIAS)

            col2Image1.image(resized_image, caption='Default Image', use_column_width=False, width=frame_size[0])

            col3, col4 = st.columns([1, 2])
            with col3:
                with st.spinner("Processing..."):
                    if col1.button('🔃 Process Image'):
                        yolo_output = get_yolo_output(uploaded_image.name)
                        print(yolo_output[0]['name'])
                        try:
                            if len(yolo_output) <= 0 or yolo_output is None:
                                col2Image2.info("Sorry No Inference Available :loudspeaker:\nI am Still Learning\nTry another example")
                            
                            else:
                                col2.subheader("Detected Products:")
                                if len(yolo_output) > 1:
                                    for index, yolo_output_it in enumerate(yolo_output):
                                        X1, y1, x2, y2 = yolo_output_it['box_points']
                                        yolo_output_product = get_mapping(yolo_output_it)
                                        print()

                                        url = get_product_link(yolo_output_it['name'])
                                        print("Getting Url From Database: ", url)

                                        col2.write(f"Product Detected: {yolo_output_product}, Confidence Level: {yolo_output_it['percentage_probability']}")

                                        # Generate a unique key for the button using the index
                                        button_key = f"button_{index}"

                                        if col2.button(label=yolo_output_it['name'], key=button_key, help=url[0][0], on_click=lambda url=url[0][0]: open_url(url)):
                                            pass  # Placeholder to prevent rendering content below


                                        
                                
                                elif len(yolo_output) == 1:
                                    print(yolo_output[0]['name'])
                                    url = get_product_link(yolo_output[0]['name'])
                                    print("Getting Url From Databse: ",url)
                                    col2.write(f"Product Detected: {yolo_output[0]['name']}, Confidence Level: {yolo_output[0]['percentage_probability']}")
                                    if col2.button(label=yolo_output[0]['name'], help=url[0][0], on_click=lambda url=url[0][0]: open_url(url)):
                                            pass  # Placeholder to prevent rendering content below
                                
                                
                                bo_resized_image, op_image_path = get_custom_bouding_box(upload_image_path, yolo_output, frame_size, uploaded_image.name)
                                col2Image2.image(bo_resized_image, caption='Processed Image', use_column_width=False, width=frame_size[0])
                                print("-------------------------------------------------------------")
                        except Exception as e:
                            col3.write(e)

        if uploaded_image is None:
            st.warning('Please upload the image to process')
            input_path = os.path.join(path,"input")
            output_path = os.path.join(path,"Output_image")
            yolo_output_path = os.path.join(path,"Yolo_output_image")
            temp_path = os.path.join(path,"temp")
            cleanup_task = [input_path, output_path,yolo_output_path,temp_path]
            for i in cleanup_task:
                remove_files_in_folder(i)

    # Display project information
    st.info('Developed at CDAC-Hyderabad - Part of Academic Project')

# Entry point of the script
if __name__ == '__main__':
    sys.argv.append("--browser.gatherUsageStats=false")
    if runtime.exists():
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
