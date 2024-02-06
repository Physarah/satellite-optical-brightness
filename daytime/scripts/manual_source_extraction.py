# import os
# import matplotlib.pyplot as plt
# from astropy.io import fits
#
# x_clicks = []
# y_clicks = []
#
# def on_click(event):
#     if event.inaxes is not None:
#         x_clicks.append(int(event.xdata))
#         y_clicks.append(int(event.ydata))
#         print(f"Clicked at pixel location: ({int(event.xdata)}, {int(event.ydata)})")
#
# def process_fits_file(fits_file):
#     with fits.open(fits_file) as hdulist:
#         data = hdulist[0].data
#
#     plt.imshow(data, cmap='gray', origin='lower')
#     plt.title(f"Click on the image to record pixel location - {fits_file}")
#     plt.connect('button_press_event', on_click)
#     plt.show()
#
# if __name__ == "__main__":
#     fits_directory = "/Volumes/tycho/other/sarahs-ssa/01_29_24/starlink-30836-58221C/2024-01-29_06_27_17Z"
#
#     for filename in os.listdir(fits_directory):
#         if filename.endswith(".FIT"):
#             fits_file_path = os.path.join(fits_directory, filename)
#             x_clicks = []  # Clear previous clicks for each file
#             y_clicks = []
#             process_fits_file(fits_file_path)
#
#             print(f"Clicked pixel locations for {filename}:")
#             for x, y in zip(x_clicks, y_clicks):
#                 print(f"({x}, {y})")


import os
import json
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits


def on_click(event):
    if event.inaxes is not None:
        x_clicks.append(int(event.xdata))
        y_clicks.append(int(event.ydata))
        print(f"Clicked at pixel location: ({int(event.xdata)}, {int(event.ydata)})")


def process_fits_file(fits_file, fig_size, master_flat_field_normalized):
    with fits.open(fits_file) as hdulist:
        data = hdulist[0].data
    calibrated_frame = data / master_flat_field_normalized
    plt.figure(figsize=fig_size)
    plt.imshow(calibrated_frame, cmap='gray', origin='lower')
    plt.title(f"Click on the image to record pixel location - {fits_file}")
    plt.connect('button_press_event', on_click)
    plt.show()
    plt.close()  # Close the current figure before processing the next file

    # Write x_clicks and y_clicks to a JSON file
    output_filename = "/Users/physarah/Desktop/starlink-3366-51104U_locations_NEW.json"
    click_data = {'x_clicks': x_clicks, 'y_clicks': y_clicks}

    with open(output_filename, 'a') as json_file:
        json.dump({fits_file: click_data}, json_file)
        json_file.write('\n')  # Add a newline for each entry


if __name__ == "__main__":
    fits_directory = "/Volumes/tycho/other/sarahs-ssa/01_29_24/starlink-3366-51104U/2024-01-29_05_03_15Z"
    master_flat_field_normalized = np.array(fits.getdata(
        "/Volumes/tycho/other/sarahs-ssa/01_18_24/Flats/master_rband_flat.fits"))

    for filename in os.listdir(fits_directory):
        if filename.endswith(".FIT"):
            fits_file_path = os.path.join(fits_directory, filename)

            x_clicks = []  # Clear previous clicks for each file
            y_clicks = []
            process_fits_file(fits_file_path, fig_size=(30/1.5, 20/1.5),
                              master_flat_field_normalized=master_flat_field_normalized)

            print(f"Clicked pixel locations for {filename}:")
            for x, y in zip(x_clicks, y_clicks):
                print(f"({x}, {y})")
