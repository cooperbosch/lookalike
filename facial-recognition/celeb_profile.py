def create_celeb(img_arr,des,name,db):
    value = (name, img_arr, des)
    db[name] = value
    return db
