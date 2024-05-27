import gzip
import sqlite3  # or the appropriate database module
import base64

# Function to compress sequence using gzip


def compress_sequence(sequence):
    compressed = gzip.compress(sequence.encode('utf-8'))
    return base64.b64encode(compressed).decode('utf-8')


def decompress_sequence(sequence):
    decoded = base64.b64decode(sequence)
    decompressed = gzip.decompress(decoded).decode('utf-8')
    return decompressed


def test_compress_sequence(sequence):
    conn = sqlite3.connect('protein_sequences.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE protein_sequences (
        protein_id TEXT PRIMARY KEY,
        sequence TEXT
    )
    ''')
    protein_id = 'P12345'
    sequence = 'MWQDMACVKMGLLALLCVPTFFFSFGSSSIYERSVVPRAVSRSVARMDGDVIIGALFSVHHQPSAEKVAERKCGDVREQYGIQRVEAMFHTLDRINTDPNLLPNISLGCEIRDSCWHSSVALEQSIEFIRDSLISIREDKDGSKWCIDGTPSNQPPPTKKPIAGVIGPGSSSVAIQVQNLLQLFNIPQIAYSATSIDLSDKTLFKYFLRVVPSDTLQARAILDIVKRYNWTYVSAVHTEGNYGESGMEAFKELAAQEGLCIAHSDKIYSNAGEKHFDRLLRKLRERLPKARVVVCFCEGMTVRGLLMAMRRLGVHGEFLLVGSDGWADRYEVVEGYEQEAEGGITMKLQSAIVKSFDDYYLKLRLETNTRNPWFPEFWQYRFQCRLQGHPQENKNYKKVCRGNEALQENYMQDSKMGFVINAIYAMAHGLHDMHQELCPDQTGLCEAMDPIDGSKLLDYLLKASFRGVSGEEIYFDENGDTPGRYDIMNLQMEEGRYDYLNVGSWHEGILNMDDNKLWMNSSEMVRSVCSDPCFKGQIKVIRKGEVSCCWICTTCKDNEIVQDEFTCKACELGWWPDDDLAGCQPLPLKYLDWADVESIVAVVFSCVGILITSFVTFVFIQYRDTPVVKSSSRELCYIILAGIFLGYICPFTLIARPTVISCYLQRLFVGLSSAMCYSALVTKTNRIARILAGSKKKICTRKPRFMSAWAQVIIAFMLISMQLTLEITLIILEPPEPIKSYPSIREVYLICNTSNIGMVAPLGYNGLLIMSCTYYAFKTRNVPANFNEAKYIAFTMYTTCIIWLAFVPIYFGSNYKIITTSFSVSLSVTVALGCMFTPKMYIIIAKPERNVRSAFTTSDVVRMHVGDGKSAQCGSNSFLNMFRRKKPSSGNANSNGKSVSWSESGPRQPPRGGNVWHRLSVHVRKQEAGLNQTAVIRPLTNNPDPHSCKPTGCDHGTDLHHPQGPRTAKPLYSQVEEEDDEGDVQRPLWNPSLSGQMSRLESVLDKTPYLPSHLKSHTTGHLQGAAVDTHSSHVPTMNDHTHRLEASPALEPLSVTPSELPLAPPVRALEEHGSEEEELDLLQSYIYNARGEGEAQDGEMEDITQHKTTLEESFALSPPSPFRDSVCSSDSPGLESMLGSPPSPVFTSNTLQDFAHSSSTL'

    compressed_sequence = compress_sequence(sequence)
    cursor.execute('''
        INSERT INTO protein_sequences (protein_id, sequence)
        VALUES (?, ?)
    ''', (protein_id, compressed_sequence))
    conn.commit()
    conn.close()


def update_protein_sequence(sequence):
    conn = sqlite3.connect('protein_sequences.db')
    cursor = conn.cursor()
    cursor.execute('SELECT protein_id, sequence FROM protein_sequences')
    rows = cursor.fetchall()

    # Update each sequence with its compressed version
    for protein_id, sequence in rows:
        compressed_sequence = compress_sequence(sequence)
        cursor.execute('''
            UPDATE protein_sequences
            SET sequence = ?
            WHERE protein_id = ?
        ''', (compressed_sequence, protein_id))
        conn.commit()
    conn.close()


def deduce_sequence_length():

    protein_id = "P12345"

    try:
        conn = sqlite3.connect('protein_sequences.db')
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM protein_sequences WHERE protein_id = ?", (protein_id,))

        record = cur.fetchone()

        if record:
            new_record = dict(zip([col[0] for col in cur.description], record))
            dec_seq = decompress_sequence(new_record["sequence"])
            print(f"Length of sequence is: {len(dec_seq)}")
        else:
            print(f"No record found with ID: {protein_id}")
        conn.close()
    except sqlite3.Error as error:
        print(f"Error connecting to database: {error}")


# deduce_sequence_length()
