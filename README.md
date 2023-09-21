# ==Δόμή της εργασίας==
#### Πλευρά απλού χρήστη
- Εγγραφή και είσοδος στο σύστημα	
- Σχετικά με την µη εξουσιοδοτηµένη πρόσβαση
- Προφίλ του χρήστη	
- Αναζήτηση βιβλίου	
- Εμφάνιση στοιχείων βιβλίου	
- Επιστροφή βιβλίου	
- Διαγραφή του λογαριασμού του από την υπηρεσία	
#### Πλευρά του διαχειριστή	
- Έξοδος από το σύστημα	
- Εισαγωγή βιβλίου	
- Ανανέωση ημερών κράτησης ενός βιβλίου	
- Διαγραφή βιβλίου	
- Αναζήτηση βιβλίων
- Εμφάνιση στοιχείων βιβλίου
- Εγκατάσταση
- Περιεχόμενο
- ==Σχετικά με την εργασία==










# Πλευρά απλού χρήστη.
### Εγγραφή και είσοδος στο σύστημα
Για εγγραφή στο σύστημα ο απλός χρήστης θα χρησιμοποιηθεί:
- Όνομα χρήστη
- Επώνυμο χρήστη
- Email
- Κωδικός εισόδου
- Ημερομηνία γέννησης

![Login](https://lh3.googleusercontent.com/drive-viewer/AITFw-yqa0P0FBIIu6Uih5GObq5GWjW8W8H6T2POo3KDrDt6nfXphCw3Na_AHGZp9bNtmfpzuSBgEWqtM7_k4Qgl4qws32BJvQ=s2560)

Στην συνέχεια αν ο χρήστης εγγράφηκε με την επιτυχία θα εμφανιστεί ένα μήνυμα από πάνω:
- "You were signed up. Please log in".

![Login](https://lh3.googleusercontent.com/drive-viewer/AITFw-wkpW1SYP2yb7PoAizys3fJ0kTBNZxWrFk_txibMjQapM16_We_GbDgvz4FwEeU05Ic_uvoZNDzOqW8tEishcgF9CybBw=s2560)

Στέλνοντας στοιχεία ο χρήστης λαμβάνε by default ένα field με όνομα “role” με τιμή “user”. Μόνο ο διαχειριστής είναι ήδη γραμμένος και έχει τιμή “admin”:
```flask
@app.route("/signup", methods=["post"])
def signup_action():
name = request.form["name"]
surname = request.form["surname"]
birthday = request.form["birthday"]
pwd = request.form["pwd"]
email = request.form["email"]
# role will be setted up automatically,
# in this project exists only one admin:
role = "user"

# login if username and email do not exist in db,
# login if all fields are filled
if request.method == "POST":
emailCheck = db["user"].find_one({"email": email})
if emailCheck:
return jsonify({"output": "This email " + email + " is in use."})
if emailCheck != None:
return jsonify({"output": "Some of the inputs are null. Please try again."})
else:
db["user"].insert_one(
{
"name": name,
"surname": surname,
"birthday": birthday,
"pwd": pwd,
"email": email,
"role": role,
}
)
return jsonify({"output": "You were signed up. Please log in."})
   ```
   
![image](https://lh3.googleusercontent.com/drive-viewer/AITFw-xPmVdmkWe4jOpmIcpbVr-aJg55YvuMnfcom8YgmCDVpMEre7vybYUJcxUR1bRlsbQZLDqvRCfJekewOIW-SVlx1X1Z=s1600)

Στην περίπτωση αν ο χρήστης υπάρχει ήδη στο σύστημα, τότε θα εμφανιστεί το μήνυμα: 
- "This email xxx is already in use".
![image](https://lh3.googleusercontent.com/drive-viewer/AITFw-xSu8DVDIKu2IH0e-MLNO58qyRpgm4Zw6w72-CSzTGdGr2EXiwfYwG91MPTdPNDmj3X0RtMsViJlkuEw--BvF7oll2OUA=s2560)

Το επόμενο βήμα είναι να πάει στο login σελίδα και να μπει στην εφαρμογή.

Αν θα κάνει λάθος στο στοιχεία του θα εμφανιστούν τα επόμενα μηνύματα:
- "Wrong password" ή
- ![image](https://lh3.googleusercontent.com/drive-viewer/AITFw-w9wRIuD0VVGQTUkNTSyLSNMUzZvt327aGlCoHL6n-YKwsRDgBUYGNGG9_hkNXNTZvdzWyXdB87t8G4919lXiAXlAsOmw=s2560)

- "There is no such a user"
- ![image](https://lh3.googleusercontent.com/drive-viewer/AITFw-ykuSqoKkl_R5vpLrwY2wkhdIYJ1WGxM6GHQAR7NCqz1QpiPNwxuFVDFwWuLdGY_ROQLxlkdQsDZThx49KA5_xEFM50=s2560)

### Σχετικά με την µη εξουσιοδοτηµένη πρόσβαση
Ο χρήστης του συστήματος (απλός χρήστης ή διαχειριστής) πρέπει πρώτα να εισαχθεί στο σύστημα για να κάνει  επιθυμητές ενέργειες. Για αυτό τον λόγο υπάρχει ένα decorator:
```flask
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        # if user is not logged in, redirect to login page
        user = db["user"].find_one({"_id": ObjectId(session["mongodb_id"])})
        if not user:
            flash("Please authorize")
            return redirect("login", code = 401)
        return f(*args, **kwargs)

    return wrap
   ```
![image](https://lh3.googleusercontent.com/drive-viewer/AITFw-yZgUhpQ3SbSJM9oMrbvAMHIZt0AgKqIdbgulXTijSR5ZKnWTj02MlPPQvYalVQ8wxCuwC1Qumf0e_OmR19ab2LsbvxFg=s1600)

![image](https://lh3.googleusercontent.com/drive-viewer/AITFw-wexYgLTDGTGVOtxnA0lx7eD-3QO16HI4LQX291Xrum3DwQESqMKxN17mozSl3bydGKeFDt2V_gCOxWJi7jC_NkGd34LA=s2560)

Αυτό το decorator είναι σε κάθε σελίδα η οποία θέλει εξουσιοδοτημένη πρόσβαση, π.χ. το προφιλ του χρήστη:
```flask
@app.route("/profile")
@login_required
   ```
Ο απλός χρήστης δεν έχει πρόσβαση στις σελίδες του διαχειριστη. Για αυτό τον λόγο κάθε χρήστης έχει πεδίο με όνομα ‘role’:
```flask
   def admin_login_required(f):
@wraps(f)
def wrap(*args, **kwargs):
user = db["user"].find_one({"_id": ObjectId(session["mongodb_id"])})
user_role = user.get("role")
if user_role != "admin":
#flash("Unauthorized access. Only admin can access this page.")
abort(403)
return f(*args, **kwargs)
return wrap
   ```
   Αποτέλεσμα αν ο χρήστης προσπαθεί να μπει στην σελίδα χωρίς login:

![image](https://lh3.googleusercontent.com/drive-viewer/AITFw-zrJX8fvcfqo9So7yKT3ISMRv-dDgQoleJjNBbL6_ZMIt89BqNyIVQM2Zacc96ryMMNB7XzkrvoW42nIr41bPYVmeqG=s1600)
### Προφίλ του χρήστη

Εμφάνιση της σελίδας μετά της εγγραφής (αν ο χρήστης δεν έκανε κράτηση βιβλίου):

![image](https://lh3.googleusercontent.com/drive-viewer/AITFw-wbixQpHsrU7Zr7Gb_jtSC0uypHPGaGjzoyeLUl2ovxDhdO6PKPjMaYVfg1a52uYBmwEzHmmFAZ8qElBq2Xy3_TSQHR0g=s1600)

Επίσης, σε κάθε σελίδα ο χρήστης μπορεί να εξέλθει ( μαύρο κουμπί στο header “Log out”). Επομένως όλες οι επόμενες ενέργειες στην εφαρμογή θα γίνουν μη διαθέσιμα.
![image](https://lh3.googleusercontent.com/drive-viewer/AITFw-wtf-_3Y2UVtJFN0iAeccuEyygvMMByTq-9SlOWtJD3audy5y69rn81R9TlV88dEvdN4QOtjFiZ91Ck5p0kkCm6QoC6yQ=s2560)
### Αναζήτηση βιβλίου
Στην σελίδα “profile” o χρήστης μπορεί να αναζητά τα βιβλία με 4εις τρόπους:
- Τίτλο, ή
- Συγγραφέα, ή
- Ημερομηνία έκδοσης, ή
- ISBN, ή
- Εμφάνιση όλων των διαθέσιμων βιβλίων (πατώντας μαύρο κουμπί “Search”)

![img](https://lh3.googleusercontent.com/drive-viewer/AITFw-zPa8sRr14iwmMLDLKMamQv6BoPGelwCnODh5aVpyuyxACZvfSzekBo7MTOXfPzwdJIRhqH0se8ujteHKamhpi0qLeu6Q=s1600)

Άρα ο χρήστης μπορεί να ψάχνει βιβλία με τα δικά του κρητέρια.
Επίσης, το _id θεωρείται σαν ISBN και αφού το _id είναι ObjectId πρέπει να τροποποιηθεί με χρήση ObjectId(isbn):
```flask
if isbn:
 book_find = db["book"].find({"_id": ObjectId(isbn)})
 return render_template("show_flight.html", books=book_find)
   ```
Για παράδειγμα ψάξουμε να βρούμε ένα βιβλίο με βάση χρόνου (1995):

![image](https://lh3.googleusercontent.com/drive-viewer/AITFw-zSWh6zcbWRikscARPXYF35tmcpTWaKIC8qE_KSVjDCSSSSBzwkMd_SMfBhNhlkyszC36Dty0l7PVv6f84NM8MzwhOSfQ=s1600)
   
###  Εμφάνιση στοιχείων βιβλίου
Αν ο χρήστης επιθυμεί να δει ολόκληρη πληροφορία για συγκεκριμένο βιβλίο μπορεί να πατάει κουμπί “ See more”.
Θα δει επίσης:
- Αν είναι διαθέσιμο προς κράτηση (αν όχι στην στήλη “Option” θα έχει “Wait for updates”)
- Για πόσες μέρες μπορεί να κρατηθεί, και
- Τη περίληψη του

Στην περίπτωση, αν το βιβλίο είναι διαθέσιμο προς κράτηση ( δηλαδή, δεν το έχει πάρει κανένας) ο χρήστης μπορεί να το κρατήσει πατόντας το κουμπί“Borrow” και στην συνέχεια εισάγοντας το κινητό επικοινωνίας του (τα υπόλοιπα στοιχεία θα υπάρχει ήδη στη ιστοσελίδα).
![image](https://lh3.googleusercontent.com/drive-viewer/AITFw-yE4ONO8xVc-3b3br1FX_AYgKb0JrMF6x6B0her3XsG7ErPJZ3gOIdYRmqytZFZENszPpkES-FPk5_ZWVVz8-KK6qYq=s1600)

Μετά της κράτησης θα εμφανιστεί το μήνυμα:
- “Done!”

και τώρα ο χρήστης μπορεί να βρεθεί αυτό το βιβλίο στο προφίλ του.

![image](https://lh3.googleusercontent.com/drive-viewer/AITFw-yOVObETBQQab6ugSmDK4K9f57ycyK_23j56_B9IEtevDibTk2CzEshp7V9IDMxX6Bcv7UcK7Fllkyrya4OFr-we4JoiA=s2560)

Επίσης θα δει:
- Τίτλος βιβλίου,
- Συγγραφέας,
- Ημερομηνία έκδοσης,
- ISBN,
- Ημερομηνία κράτησης ( με χρήση from datetime import datetime, timedelta)
- Σε πόσες ημέρες θα πρέπει να επιστρέψει ο χρήστης το βιβλίο στη δανειστική βιβλιοθήκη

![image](https://lh3.googleusercontent.com/drive-viewer/AITFw-z2CNVLX1m4b9cfBffMVhz77Zmco90jvc5L4KV4NyMp0uDZR3GBUT1oDfE6jrkdKNMdN-N01KnRV4ynHwfTULt2UkGCCQ=s1600)

Άρα, μαζί με το ObjectId στην συλλογή “reservation” θα πάε και το id_book (από την συλλογη “book”)
και id_user (από την συλλογη “user”)
![image](https://lh3.googleusercontent.com/drive-viewer/AITFw-yzmSOsuU9f2fz-EMst_gY-aYV8GIcj-UsHAZ8EralMMEPLA7NXa6zIQs5Y1I161N4CuIiSOvzUbdgvpDEFAZXTOike=s1600)

### Επιστροφή βιβλίου
Όταν ο χρήστης ´κάνει κράτηση βιβλίου, στην συλλογή “book” αλλάζει field “isAvailable” από “Yes” στο “No”.
```flask
# change the availability of book:
db["book"].update_one(
{"_id": id_book},
{"$set": {"isAvailable": "No"}},
)
   ```
   
Επομένως, ο χρήστης μπορεί να κάνει κράτηση μόνο όταν field “isAvailable” έχει τιμή “Yes”.
Μετά όμως, ο καθένος δεν μπορεί να κρατάει αυτό το βιβλίο.
Πατώντας “Return Book” αλλάζουμε το field “isAvailable” == “Yes” στο συλλογή ‘book’. Στην συνέχεια στην συλλογή “reservation” σβήσουμε αυτή την κράτηση:
```flask
@app.route("/cancel_flight/")
def cancel_flight():
id = request.args.get("id")
get_land_id = db["reservation"].find_one({"_id": ObjectId(id)})
book = get_land_id.get("id_book")
db["book"].update_one({"_id": ObjectId(book)}, {"$set": {"isAvailable": "Yes"}})
db["reservation"].delete_one({"_id": ObjectId(id)})
flash("Reservation was canceled.")
return redirect(url_for("profile"))
   ```
   
### Διαγραφή του λογαριασμού του από την υπηρεσία
Ο χρήστης αν επιθυμεί μπορεί να διαγραφεί το λογαριασμό του. Οι κρατήσεις που έχουν γίνει από το συγκεκριμένο χρήστη δε θα επηρεάζονται.

# Πλευρά του διαχειριστή
Η είσοδος στο σύστημα γίνονται ως στην πλευρά του απλού χρήστη εκτός ο διαχειριστής είναι ήδη γραμμένος και έχει τα επόμενα στοιχεία:
![image](https://lh3.googleusercontent.com/drive-viewer/AITFw-zvB8x41nuKxDHDb2cRwklnCE290hXu0KTu2K6GYwX-6IKpEG_RFhkp_EvVUuwkfBCpbUhCHVVcDvyMcSjMX_JZWOZaWg=s1600)

- email: admin@mail.com
- pwd: 123456

### Έξοδος από το σύστημα
O διαχειριστής μπορεί να εξέλθει από το σύστημα πατόντας “Log Out”.
### Εισαγωγή βιβλίου
Ο διαχειριστής θα μπορεί να εισάγει καινουργια βιβλία και θα είναι διαθέσιμα και στους απλούς χρήστες.

![image](https://lh3.googleusercontent.com/drive-viewer/AITFw-zlnbCMLR1ZbF_aNzc32ITVtCAG0HXqPkOXSiBYIJeS3g40tFZlBuLQW4KLCGufO_4FZzucjf7XFIgszAyaUaFqeSII=s2560)

### Ανανέωση ημερών κράτησης ενός βιβλίου
Ανανέωση ημερών κράτησης γίνεται στην σελίδα του προφίλ του διαχειριστή με χρήση ajax.
```flask
$(document).ready(function () {
$('.updatePrice').on('click', function (e) {
$('.secretDiv').show();
id = $(this).attr('value');
});
$('form').on('submit', function (e) {
$.ajax({
data: {
id: id,
be_land: $('#be_land').val(),
},
type: 'POST',
url: '/admin_update_price'
})
.done(function (data) {
$('.secretDiv').text(data.output).show();
setTimeout(function () { location.reload(); }, 2000);
});
e.preventDefault();
});
});
   ```
Πριν αλλαγής (Qjuery):
![image](https://lh3.googleusercontent.com/drive-viewer/AITFw-zGlN-iFv6qF3KfP_o7t4UJx5wwJO9MDWyPiUkOWTeFN0CrJJoAFgmIvDXjuFgndQp_yKppgrzC7k_W3Yd6XzrNqFBe=s1600)
Αμέσως μετά:
![image](https://lh3.googleusercontent.com/drive-viewer/AITFw-ycBvteZTza1RxkDUfqxCYqa-aTkKPp2clN-6MXr8oYPlICLr06Kwv7EqfrEPQuyECYqhgWyrJtqG9plvKdN1bKgv0B=s1600)

### Διαγραφή βιβλίου
Ο διαχειριστής θα μπορεί να διαγράψει ένα βιβλίο από το σύστημα, μόνο αν δεν είναι κρατημένο από κάποιον χρήστη:
```Flask
@app.route("/admin_delete_flight/")
def admin_delete_flight():
id = request.args.get("id")
book = db["reservation"].find_one({"id_book": ObjectId(id)})
# book can be deleted only if it is not borrowed already:
if book != None:
flash("This book was landed and can't be deleted.")
return redirect(url_for("admin_profile"))
else:
db["book"].delete_one({"_id": ObjectId(id)})
flash("Book was deleted.")
return redirect(url_for("admin_profile"))
   ```
Αν είναι ήδη δανιζμένο, τότε:
![image](https://lh3.googleusercontent.com/drive-viewer/AITFw-xVDlXvBwK4MLF6JEgaw-JANxfXs0TLrLP-VC-8WtJGEcSG9L1d1l3IRrXvERtvCUu2tphvg3NVrdv3bPu0kD2sHVk-=s1600)
   
Αν ήταν διαθέσιμό από πριν:
![image](https://lh3.googleusercontent.com/drive-viewer/AITFw-xsswHPriNN6yMGJBmUWrbcIgD1QWFxBjzmyxP4fL8fSE0gC46qr4XcJqAabSKAMMuEx0vCa_wBW6FClt8k51WjsxEq=s1600)
### Αναζήτηση βιβλίων
Στην σελίδα του διαχειριστή αυτός θα μπορεί να αναζητά τα βιβλία με 3εις τρόπους:
- Τίτλο βιβλίου,
- Συγγραφέα,
- ISBN,
- Εμφάνιση όλων των διαθέσιμων προς κράτηση βιβλίων

![image](https://lh3.googleusercontent.com/drive-viewer/AITFw-yCcgA7ADfLiahPPxTwKtR_qlPd_Z3LFcIY5w7gkFh0gncw7pVPJX0lYxSJYBVMhezoUFP_7_q1z7F9S3OJGYOS51QY2Q=s1600)

### Εμφάνιση στοιχείων βιβλίου
Στοιχεία για το συγκεκριμένο βιβλίο:
- Τίτλο βιβλίου,
- Συγγραφέα,
- Ημερομηνία έκδοσης,
- ISBN,
- Περίληψη,
- Αριθμό σελίδων,
- Για πόσες ημέρες θα μπορεί κάποιος να το δανειστεί,
- Αν είναι ήδη κρατημένο ή όχι

Σε περίπτωση που το έχει ήδη κρατήσει κάποιος, να εμφανίζονται τα
στοιχεία του χρήστη που έχει κάνει τη κράτηση (όνομα, επώνυμο,
τηλέφωνο επικοινωνίας, email).

![image](https://lh3.googleusercontent.com/drive-viewer/AITFw-xYpY2ahPMaxdkru6QsWjbH0KVb1kTENpwmiPAuXQ-xET--4VV8p9-qnAvRnj-pLqtg9SFr4yvhF3WmpAUaf8VyW9pndg=s1600)

# Εγκατάσταση
Run in terminal:
- docker-compose build 
- docker-compose up
- docker-compose down (if it’s needed)

Example:
![image](https://lh3.googleusercontent.com/drive-viewer/AITFw-w6NOurLat2FtTiK_M2v7qb9-aIrDEko8EcIsHuvtbgcgj77MdaliOF-WFb5gSIKOVHYzM39m16F9ZGR2l8I_iAstL2QA=s1600)
![image](https://lh3.googleusercontent.com/drive-viewer/AITFw-wOQ3cSW-G46jO4Pf7ND3RAxsQ8zstpuj4MMlQ3MqEZ-kDxMJGKk9xRprOZ6CaM9CulVv11rsQspweMADxXPJvGt85tvQ=s1600)
# Περιεχόμενο
- static (css)
- templates (html)
- app.py (code)
- docker.compose.yml
- Dockerfile
- requirements.txt

Μετά της εντολής docker-compose build:
- data (file)

# ==Σχετικά με την εργασία==
- Η εργασία αυτή ήταν φτιαγμένη πάνω ==σε εργασία Εαρ. Εξ. 2022-2023== την οποία δεν έστειλα. Για αυτό τον λόγο μέσα της εργασίας και στην αναφορά μπορείτε να δείτε κάποιες μεταβλητές με ονόματα ==“flight”, “ticket”== και άλλα ονόματα τα οποία έχουν σχέση με προηγούμενο θέμα [Ιούνιος 2023].
- Στην αρχή η εργασία ήταν συνδεδεμένα με mongodb cloud:
```Flask
connection_string = "mongodb+srv://viktorijapopova5:simple_pass@cluster0.da1byij.mongodb.net/?retryWrites=true&w=majority"
   ```
Στην αρχή είχα προβλήματα να δημιουργήσω docker για την βάσή δεδομένων, το συνδέφικα με cloud για να προχωρήσω με την εργασία αυτή.
- Στην εργασία (app.py γραμμή  29) υπάρχει μεθοδος “insert_many” για να υπάρχουν default βιβλία, χρήστες και   διαχειριστής στην βάση.
- docker-compose.yml περιέχει  mongo-express image για οπτική εμφάνιση:

![image](https://lh3.googleusercontent.com/drive-viewer/AITFw-xVs1xyjv5Uk2vpNiEkYdHljG4v3rDYuFNl2arlviJdSBeCPqmtXq2C-96Adk_w0HT3RZFISNXAK8m3zgfapLLQiKgm2A=s1600)

