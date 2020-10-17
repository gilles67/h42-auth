from OpenSSL import crypto


 def generate_csr():



     req = crypto.X509Req()
     req.set_version(2)
     subject = req.get_subject()
     subject['C'] = "FR"
     subject['L'] = "Schiltigheim"
     subject['CN'] = "Gilles GAUVENET"
     subject['O'] = "75df58.h42.link"
     subject['emailAddress'] = "gilles@75df58.h42.link"



if __name__ == '__main__':
