# Import necessary libraries
import numpy as np
import layoutparser as lp
from PIL import Image
import io
from flask import Flask, request, jsonify, send_file
import fitz  # PyMuPDF
