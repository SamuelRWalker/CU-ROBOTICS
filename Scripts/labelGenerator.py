from lxml import etree as et

def labelXML():
    root = et.Element('annotation',{'verified':'yes'})
    folder = textSubElement(root, 'folder', 'folderName')
    filename = textSubElement(root, 'filename', 'fileName')
    path = textSubElement(root, 'path','filePath')
    source = et.SubElement(root, 'source')
    database = textSubElement(source, 'database','Unknown')
    size = et.SubElement(root, 'size')
    width = textSubElement(size, 'width','widthhh')
    height = textSubElement(size, 'height','heighttt')
    depth = textSubElement(size, 'depth','3')
    segmented = textSubElement(root, 'segmented','0')
    object = et.SubElement(root, 'object')
    name = textSubElement(object, 'name', 'color')
    pose = textSubElement(object, 'pose', 'Unspecified')
    truncated = textSubElement(object, 'truncated', '0')
    difficult = textSubElement(object, 'difficult', '0')
    bndbox = et.SubElement(object, 'bndbox')
    xmin = textSubElement(bndbox, 'xmin', 'value')
    ymin = textSubElement(bndbox, 'ymin', 'value')
    xmax = textSubElement(bndbox, 'xmax', 'value')
    ymax = textSubElement(bndbox, 'ymax', 'value')
    return root

def textElement(tag, text, *args, **kwargs):
    element = et.Element(tag, *args, **kwargs)
    element.text = text
    return element

def textSubElement(parent, tag, text, *args, **kwargs):
    element = et.SubElement(parent, tag, *args, **kwargs)
    element.text = text
    return element

def saveXML(filepath,filename):
    root = labelXML()
    file = open(filepath+filename+".xml", "wb")
    et.indent(root, space="    ")
    file.write(et.tostring(root,pretty_print=True),)
    return