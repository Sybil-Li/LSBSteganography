# LSBSteganography
Implementation of a general least significant bit algorithm for steganography.
The program requires PIL (Python Image Library) and NumPy.

To run the program: 

        python -i steg.py

        # This would generate a steg image with secret image hidden in cover image,
        # saved to the same directory as the program as steg.bmp.
        >>> embed()   

        # This would recover the secret image from the steg image,
        # saved to the same directory as the program as secret.bmp.
        >>>> recover() 

To change settings:

      # Default is cover_image_path = 'mares.bmp'
      cover_image_path = “your_cover_image.bmp”
      
      # Default is secret_image_path = 'lena.bmp'
      secret_image_path = “your_secret_image.bmp”
      
      # Default is steg_image_path = 'steg.bmp'
      steg_image_path = “your_steg_image.bmp”
      
      # Default is num_sb = 4
      num_sb = 1 (or 2 or 4)
