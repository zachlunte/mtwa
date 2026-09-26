#!/usr/bin/env python3

from flask import Flask, render_template, send_from_directory, request, redirect, url_for
from fpdf import FPDF
import math
import os

# Create a Flask application instance
app = Flask(__name__)

# Create a function to add a label to the appropriate location in PDF
def add_label(pdf,i,product_description,product_price):
    product_price = "${}".format(product_price)
    if i % 2 == 0:
        pdf.line(8,8*(1+math.floor(i/2))+(64*math.floor(i/2)),(pdf.w/2)-8,8*(1+math.floor(i/2))+(64*math.floor(i/2)))
        pdf.line(8,8*(1+math.floor(i/2))+(64*(math.floor(i/2)+1)),(pdf.w/2)-8,8*(1+math.floor(i/2))+(64*(math.floor(i/2)+1)))
        pdf.line(8,8*(1+math.floor(i/2))+(64*math.floor(i/2)),8,8*(1+math.floor(i/2))+(64*(math.floor(i/2)+1)))
        pdf.line((pdf.w/2)-8,8*(1+math.floor(i/2))+(64*math.floor(i/2)),(pdf.w/2)-8,8*(1+math.floor(i/2))+(64*(math.floor(i/2)+1)))
        p_halves = product_description.split('[')
        p_half1 = p_halves[0]
        p_half1_chunks = p_half1.split(';')
        total_chunks = []
        j = 0
        climit = 24
        if len(product_description) >= 128:
            climit=30
        for chunk in p_half1_chunks:
            if len(chunk) > climit and (j < 4 or j >= 8):
                total_chunks.append(chunk[0:climit-1]+"-")
                second_chunk = chunk[climit-1:]
                if len(second_chunk) > climit:
                    total_chunks.append(second_chunk[0:climit-1]+"-")
                    total_chunks.append(second_chunk[climit-1:])
                    j = j + 2
                else:
                    total_chunks.append(chunk[climit-1:])
                    j = j + 1
            else:
                total_chunks.append(chunk)
                j = j + 1
        if len(p_halves) > 1:
            p_half2 = "["+p_halves[1]
            p_half2 = p_half2.replace("[","")
            p_half2 = p_half2.replace("]","")
            p_half2_chunks = p_half2.split(';')
            for chunk in p_half2_chunks:
                if len(chunk) > climit and (j < 4 or j >= 8):
                    total_chunks.append(chunk[0:climit-1]+"-")
                    second_chunk = chunk[climit-1:]
                    if len(second_chunk) > climit:
                        total_chunks.append(second_chunk[0:climit-1]+"-")
                        total_chunks.append(second_chunk[climit-1:])
                        j = j + 2
                    else:
                        total_chunks.append(chunk[climit-1:])
                        j = j + 1
                else:
                    total_chunks.append(chunk)
                    j = j + 1
        font_size = 12
        if len(total_chunks) > 9:
            font_size = 10
        chunk_level = 0
        iterat = 0
        for chunk in total_chunks:
            if iterat == 0:
                pdf.set_font("Arial", style="B", size=font_size)
            else:
                pdf.set_font("Arial", size=font_size)
            pdf.set_xy(12,font_size*(1+math.floor(i/2))+(64*math.floor(i/2))-(4*math.floor(i/2))+chunk_level)
            pdf.cell(24,font_size,txt=chunk.strip())
            chunk_level = chunk_level + (math.floor(font_size/2))
            iterat = iterat + 1
        pdf.set_xy((pdf.w/2)-36,8*(1+math.floor(i/2))+(64*(math.floor(i/2)+1))-18)
        pdf.set_font("Arial",style="B",size=24)
        pdf.cell(24,16,txt=product_price)
        pdf.image("res/applet.png", x=(pdf.w/2)-36, y=12*(1+math.floor(i/2))+(64*math.floor(i/2))-(4*math.floor(i/2)), w=20)
    else:
        pdf.line((pdf.w/2)+8,8*(1+math.floor(i/2))+(64*math.floor(i/2)),(pdf.w)-8,8*(1+math.floor(i/2))+(64*math.floor(i/2)))
        pdf.line((pdf.w/2)+8,8*(1+math.floor(i/2))+(64*(math.floor(i/2)+1)),(pdf.w)-8,8*(1+math.floor(i/2))+(64*(math.floor(i/2)+1)))
        pdf.line((pdf.w/2)+8,8*(1+math.floor(i/2))+(64*math.floor(i/2)),(pdf.w/2)+8,8*(1+math.floor(i/2))+(64*(math.floor(i/2)+1)))
        pdf.line((pdf.w)-8,8*(1+math.floor(i/2))+(64*math.floor(i/2)),(pdf.w)-8,8*(1+math.floor(i/2))+(64*(math.floor(i/2)+1)))
        p_halves = product_description.split('[')
        p_half1 = p_halves[0]
        p_half1_chunks = p_half1.split(';')
        total_chunks = []
        j = 0
        climit = 24
        if len(product_description) >= 128:
            climit=30
        for chunk in p_half1_chunks:
            if len(chunk) > climit and (j < 4 or j >= 8):
                total_chunks.append(chunk[0:climit-1]+"-")
                second_chunk = chunk[climit-1:]
                if len(second_chunk) > climit:
                    total_chunks.append(second_chunk[0:climit-1]+"-")
                    total_chunks.append(second_chunk[climit-1:])
                    j = j + 2
                else:
                    total_chunks.append(chunk[climit-1:])
                    j = j + 1
            else:
                total_chunks.append(chunk)
                j = j + 1
        if len(p_halves) > 1:
            p_half2 = "["+p_halves[1]
            p_half2 = p_half2.replace("[","")
            p_half2 = p_half2.replace("]","")
            p_half2_chunks = p_half2.split(';')
            for chunk in p_half2_chunks:
                if len(chunk) > climit and (j < 4 or j >= 8):
                    total_chunks.append(chunk[0:23]+"-")
                    second_chunk = chunk[23:]
                    if len(second_chunk) > 24:
                        total_chunks.append(second_chunk[0:23]+"-")
                        total_chunks.append(second_chunk[23:])
                        j = j + 2
                    else:
                        total_chunks.append(chunk[23:])
                        j = j + 1
                else:
                    total_chunks.append(chunk)
                    j = j + 1
        font_size = 12
        if len(total_chunks) > 9:
            font_size = 10
        chunk_level = 0
        iterat = 0
        for chunk in total_chunks:
            if iterat == 0:
                pdf.set_font("Arial", style="B", size=font_size)
            else:
                pdf.set_font("Arial", size=font_size)
            pdf.set_xy((pdf.w/2)+12,font_size*(1+math.floor(i/2))+(64*math.floor(i/2))-(4*math.floor(i/2))+chunk_level)
            pdf.cell(24,font_size,txt=chunk.strip())
            chunk_level = chunk_level + (math.floor(font_size/2))
            iterat = iterat + 1
        pdf.set_xy((pdf.w)-36,8*(1+math.floor(i/2))+(64*(math.floor(i/2)+1))-18)
        pdf.set_font("Arial",style="B",size=24)
        pdf.cell(24,16,txt=product_price)
        pdf.image("res/applet.png", x=(pdf.w)-36, y=12*(1+math.floor(i/2))+(64*math.floor(i/2))-(4*math.floor(i/2)), w=20) 

def process_input_data(pd1,pp1,pd2,pp2,pd3,pp3,pd4,pp4,pd5,pp5,pd6,pp6):
     
    # Set the initial PDF properties
    pdf = FPDF()
    pdf.add_page()
    pdf.set_line_width(2)

    products = []
    products.append([pd1,pp1])
    products.append([pd2,pp2])
    products.append([pd3,pp3])
    products.append([pd4,pp4])
    products.append([pd5,pp5])
    products.append([pd6,pp6])

    # Add a label for each product
    for i in range(6):
        add_label(pdf,i,products[i][0],products[i][1])

    # Save the output to a file and terminate the program
    pdf.output("download/labels.pdf")

    return "New PDF loaded!"

# Route to force download of the PDF
@app.route('/download/<filename>')
def download_pdf(filename):
    return send_from_directory('download', filename, as_attachment=True)

# Route to label generator page
@app.route("/mtlg", methods=['GET', 'POST'])
def mtlg():
    if request.method == 'POST':
        pd1 = request.form.get('product_description_1')
        pp1 = request.form.get('product_price_1')
        pd2 = request.form.get('product_description_2')
        pp2 = request.form.get('product_price_2')
        pd3 = request.form.get('product_description_3')
        pp3 = request.form.get('product_price_3')
        pd4 = request.form.get('product_description_4')
        pp4 = request.form.get('product_price_4')
        pd5 = request.form.get('product_description_5')
        pp5 = request.form.get('product_price_5')
        pd6 = request.form.get('product_description_6')
        pp6 = request.form.get('product_price_6')
        processed_result = process_input_data(pd1,pp1,pd2,pp2,pd3,pp3,pd4,pp4,pd5,pp5,pd6,pp6)
        return render_template('mtlg.html', result=processed_result) 
    return render_template('mtlg.html', result=None)

@app.route("/mtsl")
def mtsl():
    return render_template('mtsl.html', result=None)

@app.route("/mtuf")
def mtuf():
    return render_template('mtuf.html', result=None)

@app.route("/mtdh")
def mtdh():
    return render_template('mtdh.html', result=None)

@app.route("/mlbrr")
def mlbrr():
    return render_template('mlbrr.html', result=None)

# Define a route for the root URL ("/")
@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html', result=None)

# Run the Flask application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
