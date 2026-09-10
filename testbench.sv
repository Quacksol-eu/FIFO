`timescale 1ns / 1ps

module tb_Register;

    reg clk;
    reg reset; 
    reg wr_en;
    reg rd_en;
    reg [7:0] din;
    wire [7:0] dout;
    wire full;
    wire empty;
    wire [4:0] count;

    Register uut (
        .reset(reset),
        .clk(clk),
        .wr_en(wr_en),
        .rd_en(rd_en),
        .dout(dout),
        .din(din),
        .full(full),
        .empty(empty),
        .count(count)
    );

    always #5 clk = ~clk;

    task log_state;
        input string label;
        begin
            $display("%s -> Wr: %b | Rd: %b | Din: 0x%h | Dout: 0x%h | Wr_Ptr: 0x%h (wrap:%0b) | Rd_Ptr: 0x%h (wrap:%0b) | Count: %0d | Full: %0d | Empty: %0d", 
                label, wr_en, rd_en, din, dout, 
                uut.wr_ptr[3:0], uut.wr_ptr[4], 
                uut.rd_ptr[3:0], uut.rd_ptr[4], 
                count, full, empty);
        end
    endtask

    initial begin
        $dumpfile("dump.vcd");
        $dumpvars(0, tb_Register);

        clk = 0;
        reset = 1;
        wr_en = 0;
        rd_en = 0;
        din = 8'h00;

        #25;
        reset = 0;
        #15;

        $display("\n--- 1. ZAPIS 3 ELEMENTOW ---");
        repeat (3) begin
            wr_en = 1;
            rd_en = 0;
            din = din + 8'h10; 
            @(posedge clk);
            #1;
            log_state("Zapis");
        end
        wr_en = 0;

      $display("\n 2. ODCZYT 2 ELEMENTOW ");
        repeat (2) begin
            wr_en = 0;
            rd_en = 1;
            @(posedge clk);
            #1;
            log_state("Odczyt");
        end
        rd_en = 0;

      $display("\n 3. JEDNOCZESNY ZAPIS I ODCZYT");
        repeat (5) begin
            wr_en = 1;
            rd_en = 1;
            din = din + 8'h05;
            @(posedge clk);
            #1;
            log_state("Jednoczesny");
        end
        wr_en = 0;
        rd_en = 0;

        $display("\n 4. PROBA ODCZYTU 6 ELEMENTOW ");
        repeat (6) begin
            wr_en = 0;
            rd_en = 1;
            @(posedge clk);
            #1;
            log_state("Próba odczytu");
        end
        rd_en = 0;

        $display("\n- 5. PROBA ZAPISU 20 ELEMENTOW ");
        repeat (20) begin
            wr_en = 1;
            rd_en = 0;
            din = din + 8'h01;
            @(posedge clk);
            #1;
            log_state("Próba zapisu");
        end
        wr_en = 0;

        $display("\n 6. TEST LOSOWYCH OPERACJI ");
      repeat (50) begin
            wr_en = $random % 2; 
            rd_en = $random % 2; 
            din   = $random;     
            @(posedge clk);
            #1;
            log_state("Losowy");
        end
        wr_en = 0;
        rd_en = 0;

        #50;
        $finish;
    end

endmodule