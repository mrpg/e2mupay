uproot.simulate.on("e2mupay/PaymentData", (sim) => {
    sim.fill({
        fname: "bratan",
        lname: "milošević",
        email: "gros@unimelb.edu.au",
        email_confirm: "gros@unimelb.edu.au",
    });
    I("submitButton").click();
    I("confirmSend").click();
});
