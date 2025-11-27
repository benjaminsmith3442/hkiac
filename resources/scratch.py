# canvas.create_text(170, 997, text="CURRENT", font=("Terminal", 16, "bold"), fill="white", width=600, anchor="nw",justify="left")
# canvas.create_text(360, 997, text="INSTRUCTIONS", font=("Terminal", 16, "bold"), fill="white", width=600,anchor="nw", justify="left")











# Image monochromatic
input_path = "C:\\Users\\benja\\wassup.png"       # Your uploaded file
output_path = "C:\\Users\\benja\\wassupdog_dos.png"   # Output file

def dosify_image(input_path, output_path, pixel_size=1):
    img = Image.open(input_path).convert("L")  # grayscale

    width, height = img.size

    # Pixelate by downscaling then upscaling
    img_small = img.resize(
        (width // pixel_size, height // pixel_size),
        Image.NEAREST
    )
    img_pixelated = img_small.resize(
        (width, height),
        Image.NEAREST
    )

    # Convert to pure black & white
    threshold = 64
    img_bw = img_pixelated.point(lambda p: 0 if p > threshold else 255)

    img_bw.save(output_path)
    print("Saved:", output_path)

dosify_image(input_path, output_path)










# ASM Instructions
root = tk.Tk()
root.title("Highlight Text Example")

canvas = tk.Canvas(root, width=1000, height=1000, bg="black")
canvas.pack()

# Text properties
lines = Instructions.assembly
font_style = ("Terminal", 16, "bold")
text_color = "lime"
bg_color = "black"
padding = 3

current_instruction_index = 0
text_ids = []
rect_id = None

def draw_text():
    global rect_id, text_ids
    canvas.delete("all")  # clear previous items
    text_ids = []

    # Draw all lines normally first
    for i, line in enumerate(lines):
        x, y = 200, 25 + i*25
        text_ids.append(canvas.create_text(x, y, text=line, font=font_style, fill=text_color, width=400, anchor="nw", justify="left"))

    # Draw rectangle around highlighted line
    highlighted_id = text_ids[current_instruction_index]
    bbox = canvas.bbox(highlighted_id)  # returns (x1, y1, x2, y2)
    x1, y1, x2, y2 = bbox
    rect_id = canvas.create_rectangle(
        x1-padding, y1-padding, 400, y2+padding,
        fill=text_color, outline=text_color
    )

    # Draw the highlighted text in inverted color
    x, y = (x1 + x2)//2, (y1 + y2)//2
    canvas.create_text(x, y, text=lines[current_instruction_index], font=font_style, fill="red", width=400, anchor="center", justify="left")

def move_highlight(event):
    global current_instruction_index
    if event.keysym == "Up":
        highlight_index = max(0, highlight_index - 1)
    elif event.keysym == "Down":
        highlight_index = min(len(lines) - 1, highlight_index + 1)
    draw_text()


def exit_app(event):
    root.destroy()

root.bind("<Up>", move_highlight)
root.bind("<Down>", move_highlight)


# Bind the Escape key
root.bind("<Escape>", exit_app)
draw_text()
root.mainloop()
