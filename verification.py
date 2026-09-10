import re

log_data = """
Losowy -> Wr: 0 | Rd: 1 | Din: 0x09 | Dout: 0x4a | Wr_Ptr: 0x8 (wrap:1) | Rd_Ptr: 0x9 (wrap:0) | Count: 15 | Full: 0 | Empty: 0
Losowy -> Wr: 1 | Rd: 1 | Din: 0x8d | Dout: 0x4b | Wr_Ptr: 0x9 (wrap:1) | Rd_Ptr: 0xa (wrap:0) | Count: 15 | Full: 0 | Empty: 0
Losowy -> Wr: 1 | Rd: 0 | Din: 0x01 | Dout: 0x4b | Wr_Ptr: 0xa (wrap:1) | Rd_Ptr: 0xa (wrap:0) | Count: 16 | Full: 1 | Empty: 0
Losowy -> Wr: 1 | Rd: 0 | Din: 0x3d | Dout: 0x4b | Wr_Ptr: 0xa (wrap:1) | Rd_Ptr: 0xa (wrap:0) | Count: 16 | Full: 1 | Empty: 0
Losowy -> Wr: 1 | Rd: 0 | Din: 0xf9 | Dout: 0x4b | Wr_Ptr: 0xa (wrap:1) | Rd_Ptr: 0xa (wrap:0) | Count: 16 | Full: 1 | Empty: 0
Losowy -> Wr: 0 | Rd: 1 | Din: 0xaa | Dout: 0x4c | Wr_Ptr: 0xa (wrap:1) | Rd_Ptr: 0xb (wrap:0) | Count: 15 | Full: 0 | Empty: 0
Losowy -> Wr: 1 | Rd: 1 | Din: 0x12 | Dout: 0x4d | Wr_Ptr: 0xb (wrap:1) | Rd_Ptr: 0xc (wrap:0) | Count: 15 | Full: 0 | Empty: 0
Losowy -> Wr: 1 | Rd: 0 | Din: 0xce | Dout: 0x4d | Wr_Ptr: 0xc (wrap:1) | Rd_Ptr: 0xc (wrap:0) | Count: 16 | Full: 1 | Empty: 0
Losowy -> Wr: 0 | Rd: 1 | Din: 0x5c | Dout: 0x4e | Wr_Ptr: 0xc (wrap:1) | Rd_Ptr: 0xd (wrap:0) | Count: 15 | Full: 0 | Empty: 0
Losowy -> Wr: 1 | Rd: 1 | Din: 0x65 | Dout: 0x4f | Wr_Ptr: 0xd (wrap:1) | Rd_Ptr: 0xe (wrap:0) | Count: 15 | Full: 0 | Empty: 0
Losowy -> Wr: 1 | Rd: 0 | Din: 0x80 | Dout: 0x4f | Wr_Ptr: 0xe (wrap:1) | Rd_Ptr: 0xe (wrap:0) | Count: 16 | Full: 1 | Empty: 0
Losowy -> Wr: 0 | Rd: 0 | Din: 0x9d | Dout: 0x4f | Wr_Ptr: 0xe (wrap:1) | Rd_Ptr: 0xe (wrap:0) | Count: 16 | Full: 1 | Empty: 0
Losowy -> Wr: 0 | Rd: 1 | Din: 0x0d | Dout: 0x50 | Wr_Ptr: 0xe (wrap:1) | Rd_Ptr: 0xf (wrap:0) | Count: 15 | Full: 0 | Empty: 0
Losowy -> Wr: 1 | Rd: 1 | Din: 0xd5 | Dout: 0x51 | Wr_Ptr: 0xf (wrap:1) | Rd_Ptr: 0x0 (wrap:1) | Count: 15 | Full: 0 | Empty: 0
Losowy -> Wr: 0 | Rd: 0 | Din: 0x1d | Dout: 0x51 | Wr_Ptr: 0xf (wrap:1) | Rd_Ptr: 0x0 (wrap:1) | Count: 15 | Full: 0 | Empty: 0
Losowy -> Wr: 1 | Rd: 1 | Din: 0x0a | Dout: 0x52 | Wr_Ptr: 0x0 (wrap:0) | Rd_Ptr: 0x1 (wrap:1) | Count: 15 | Full: 0 | Empty: 0
Losowy -> Wr: 0 | Rd: 0 | Din: 0xf2 | Dout: 0x52 | Wr_Ptr: 0x0 (wrap:0) | Rd_Ptr: 0x1 (wrap:1) | Count: 15 | Full: 0 | Empty: 0
Losowy -> Wr: 0 | Rd: 1 | Din: 0xd8 | Dout: 0x53 | Wr_Ptr: 0x0 (wrap:0) | Rd_Ptr: 0x2 (wrap:1) | Count: 14 | Full: 0 | Empty: 0
Losowy -> Wr: 0 | Rd: 1 | Din: 0xeb | Dout: 0x54 | Wr_Ptr: 0x0 (wrap:0) | Rd_Ptr: 0x3 (wrap:1) | Count: 13 | Full: 0 | Empty: 0
Losowy -> Wr: 0 | Rd: 0 | Din: 0xae | Dout: 0x54 | Wr_Ptr: 0x0 (wrap:0) | Rd_Ptr: 0x3 (wrap:1) | Count: 13 | Full: 0 | Empty: 0
Losowy -> Wr: 0 | Rd: 0 | Din: 0x0b | Dout: 0x54 | Wr_Ptr: 0x0 (wrap:0) | Rd_Ptr: 0x3 (wrap:1) | Count: 13 | Full: 0 | Empty: 0
Losowy -> Wr: 1 | Rd: 1 | Din: 0x4f | Dout: 0x55 | Wr_Ptr: 0x1 (wrap:0) | Rd_Ptr: 0x4 (wrap:1) | Count: 13 | Full: 0 | Empty: 0
Losowy -> Wr: 1 | Rd: 0 | Din: 0x7e | Dout: 0x55 | Wr_Ptr: 0x2 (wrap:0) | Rd_Ptr: 0x4 (wrap:1) | Count: 14 | Full: 0 | Empty: 0
Losowy -> Wr: 1 | Rd: 1 | Din: 0xd9 | Dout: 0x56 | Wr_Ptr: 0x3 (wrap:0) | Rd_Ptr: 0x5 (wrap:1) | Count: 14 | Full: 0 | Empty: 0
Losowy -> Wr: 0 | Rd: 0 | Din: 0x9f | Dout: 0x56 | Wr_Ptr: 0x3 (wrap:0) | Rd_Ptr: 0x5 (wrap:1) | Count: 14 | Full: 0 | Empty: 0
Losowy -> Wr: 1 | Rd: 0 | Din: 0xb7 | Dout: 0x56 | Wr_Ptr: 0x4 (wrap:0) | Rd_Ptr: 0x5 (wrap:1) | Count: 15 | Full: 0 | Empty: 0
Losowy -> Wr: 1 | Rd: 0 | Din: 0x5b | Dout: 0x56 | Wr_Ptr: 0x5 (wrap:0) | Rd_Ptr: 0x5 (wrap:1) | Count: 16 | Full: 1 | Empty: 0
Losowy -> Wr: 1 | Rd: 1 | Din: 0xd0 | Dout: 0x57 | Wr_Ptr: 0x5 (wrap:0) | Rd_Ptr: 0x6 (wrap:1) | Count: 15 | Full: 0 | Empty: 0
Losowy -> Wr: 1 | Rd: 1 | Din: 0x96 | Dout: 0x58 | Wr_Ptr: 0x6 (wrap:0) | Rd_Ptr: 0x7 (wrap:1) | Count: 15 | Full: 0 | Empty: 0
Losowy -> Wr: 0 | Rd: 0 | Din: 0xc8 | Dout: 0x58 | Wr_Ptr: 0x6 (wrap:0) | Rd_Ptr: 0x7 (wrap:1) | Count: 15 | Full: 0 | Empty: 0
Losowy -> Wr: 1 | Rd: 1 | Din: 0x12 | Dout: 0x59 | Wr_Ptr: 0x7 (wrap:0) | Rd_Ptr: 0x8 (wrap:1) | Count: 15 | Full: 0 | Empty: 0
Losowy -> Wr: 0 | Rd: 1 | Din: 0x39 | Dout: 0x8d | Wr_Ptr: 0x7 (wrap:0) | Rd_Ptr: 0x9 (wrap:1) | Count: 14 | Full: 0 | Empty: 0
Losowy -> Wr: 1 | Rd: 1 | Din: 0x85 | Dout: 0x01 | Wr_Ptr: 0x8 (wrap:0) | Rd_Ptr: 0xa (wrap:1) | Count: 14 | Full: 0 | Empty: 0
Losowy -> Wr: 0 | Rd: 1 | Din: 0x49 | Dout: 0x12 | Wr_Ptr: 0x8 (wrap:0) | Rd_Ptr: 0xb (wrap:1) | Count: 13 | Full: 0 | Empty: 0
Losowy -> Wr: 1 | Rd: 0 | Din: 0x58 | Dout: 0x12 | Wr_Ptr: 0x9 (wrap:0) | Rd_Ptr: 0xb (wrap:1) | Count: 14 | Full: 0 | Empty: 0
Losowy -> Wr: 0 | Rd: 0 | Din: 0x9c | Dout: 0x12 | Wr_Ptr: 0x9 (wrap:0) | Rd_Ptr: 0xb (wrap:1) | Count: 14 | Full: 0 | Empty: 0
Losowy -> Wr: 0 | Rd: 0 | Din: 0x73 | Dout: 0x12 | Wr_Ptr: 0x9 (wrap:0) | Rd_Ptr: 0xb (wrap:1) | Count: 14 | Full: 0 | Empty: 0
Losowy -> Wr: 1 | Rd: 1 | Din: 0xb3 | Dout: 0xce | Wr_Ptr: 0xa (wrap:0) | Rd_Ptr: 0xc (wrap:1) | Count: 14 | Full: 0 | Empty: 0
Losowy -> Wr: 1 | Rd: 0 | Din: 0xf7 | Dout: 0xce | Wr_Ptr: 0xb (wrap:0) | Rd_Ptr: 0xc (wrap:1) | Count: 15 | Full: 0 | Empty: 0
Losowy -> Wr: 1 | Rd: 0 | Din: 0x5a | Dout: 0xce | Wr_Ptr: 0xc (wrap:0) | Rd_Ptr: 0xc (wrap:1) | Count: 16 | Full: 1 | Empty: 0
Losowy -> Wr: 1 | Rd: 1 | Din: 0xda | Dout: 0x65 | Wr_Ptr: 0xc (wrap:0) | Rd_Ptr: 0xd (wrap:1) | Count: 15 | Full: 0 | Empty: 0
Losowy -> Wr: 1 | Rd: 1 | Din: 0xdf | Dout: 0x80 | Wr_Ptr: 0xd (wrap:0) | Rd_Ptr: 0xe (wrap:1) | Count: 15 | Full: 0 | Empty: 0
Losowy -> Wr: 1 | Rd: 0 | Din: 0xd0 | Dout: 0x80 | Wr_Ptr: 0xe (wrap:0) | Rd_Ptr: 0xe (wrap:1) | Count: 16 | Full: 1 | Empty: 0
Losowy -> Wr: 0 | Rd: 1 | Din: 0x0e | Dout: 0xd5 | Wr_Ptr: 0xe (wrap:0) | Rd_Ptr: 0xf (wrap:1) | Count: 15 | Full: 0 | Empty: 0
Losowy -> Wr: 0 | Rd: 0 | Din: 0xfd | Dout: 0xd5 | Wr_Ptr: 0xe (wrap:0) | Rd_Ptr: 0xf (wrap:1) | Count: 15 | Full: 0 | Empty: 0
Losowy -> Wr: 1 | Rd: 0 | Din: 0x4e | Dout: 0xd5 | Wr_Ptr: 0xf (wrap:0) | Rd_Ptr: 0xf (wrap:1) | Count: 16 | Full: 1 | Empty: 0
Losowy -> Wr: 1 | Rd: 0 | Din: 0xb6 | Dout: 0xd5 | Wr_Ptr: 0xf (wrap:0) | Rd_Ptr: 0xf (wrap:1) | Count: 16 | Full: 1 | Empty: 0
Losowy -> Wr: 0 | Rd: 1 | Din: 0xb8 | Dout: 0x0a | Wr_Ptr: 0xf (wrap:0) | Rd_Ptr: 0x0 (wrap:0) | Count: 15 | Full: 0 | Empty: 0
Losowy -> Wr: 0 | Rd: 1 | Din: 0x04 | Dout: 0x4f | Wr_Ptr: 0xf (wrap:0) | Rd_Ptr: 0x1 (wrap:0) | Count: 14 | Full: 0 | Empty: 0
Losowy -> Wr: 1 | Rd: 1 | Din: 0x4d | Dout: 0x7e | Wr_Ptr: 0x0 (wrap:1) | Rd_Ptr: 0x2 (wrap:0) | Count: 14 | Full: 0 | Empty: 0
"""

def parse_line(line):
    pattern = (
        r'Wr:\s*(\d+)\s*\|\s*Rd:\s*(\d+)\s*\|\s*Din:\s*(0x[0-9a-fA-F]+)\s*\|\s*'
        r'Dout:\s*(0x[0-9a-fA-F]+)\s*\|\s*Wr_Ptr:\s*(0x[0-9a-fA-F]+)\s*\(wrap:(\d+)\)\s*\|\s*'
        r'Rd_Ptr:\s*(0x[0-9a-fA-F]+)\s*\(wrap:(\d+)\)\s*\|\s*Count:\s*(\d+)\s*\|\s*'
        r'Full:\s*(\d+)\s*\|\s*Empty:\s*(\d+)'
    )
    match = re.search(pattern, line)
    if not match:
        return None
    g = match.groups()
    return {
        'Wr': int(g[0]),
        'Rd': int(g[1]),
        'Wr_Ptr': int(g[4], 16),
        'Wr_wrap': int(g[5]),
        'Rd_Ptr': int(g[6], 16),
        'Rd_wrap': int(g[7]),
        'Count': int(g[8]),
        'Full': int(g[9]),
        'Empty': int(g[10])
    }

def advance_ptr(ptr, wrap):
    ptr += 1
    if ptr > 0xF:
        ptr = 0
        wrap = 1 - wrap
    return ptr, wrap

def verify_fifo_same_line(log_text):
    lines = [l.strip() for l in log_text.strip().split('\n') if l]
    parsed = [parse_line(l) for l in lines if parse_line(l)]
    
    if not parsed:
        print("Brak danych do weryfikacji.")
        return

    errors = 0
    prev_state = parsed[0]
    
    for idx in range(1, len(parsed)):
        curr = parsed[idx]
        
        wr = curr['Wr']
        rd = curr['Rd']
        full_prev = prev_state['Full']
        empty_prev = prev_state['Empty']
        
        exp_count = prev_state['Count']
        exp_wr_ptr = prev_state['Wr_Ptr']
        exp_wr_wrap = prev_state['Wr_wrap']
        exp_rd_ptr = prev_state['Rd_Ptr']
        exp_rd_wrap = prev_state['Rd_wrap']
        
        # Niezależna ocena powodzenia zapisu i odczytu uwzględniająca stan Full/Empty
        write_success = (wr == 1) and not (full_prev == 1)
        read_success = (rd == 1) and not (empty_prev == 1)
        
        if write_success:
            exp_count += 1
            exp_wr_ptr, exp_wr_wrap = advance_ptr(exp_wr_ptr, exp_wr_wrap)
            
        if read_success:
            exp_count -= 1
            exp_rd_ptr, exp_rd_wrap = advance_ptr(exp_rd_ptr, exp_rd_wrap)

        # Weryfikacja zgodności pól "po" w tej samej linijce
        mismatches = []
        if curr['Count'] != exp_count:
            mismatches.append(f"Count: oczekiwano {exp_count}, otrzymano {curr['Count']}")
        if curr['Wr_Ptr'] != exp_wr_ptr or curr['Wr_wrap'] != exp_wr_wrap:
            mismatches.append(f"Wr_Ptr: oczekiwano 0x{exp_wr_ptr:x}(wrap:{exp_wr_wrap}), otrzymano 0x{curr['Wr_Ptr']:x}(wrap:{curr['Wr_wrap']})")
        if curr['Rd_Ptr'] != exp_rd_ptr or curr['Rd_wrap'] != exp_rd_wrap:
            mismatches.append(f"Rd_Ptr: oczekiwano 0x{exp_rd_ptr:x}(wrap:{exp_rd_wrap}), otrzymano 0x{curr['Rd_Ptr']:x}(wrap:{curr['Rd_wrap']})")

        if mismatches:
            errors += 1
            print(f"Błąd w linijce {idx + 1} [Wr: {wr}, Rd: {rd}]:")
            for m in mismatches:
                print(f"  - {m}")
        
        prev_state = curr

    if errors == 0:
        print("Wszystkie linie są poprawne!")
    else:
        print(f"Znaleziono błędnych linii: {errors}")

if __name__ == "__main__":
    verify_fifo_same_line(log_data)
