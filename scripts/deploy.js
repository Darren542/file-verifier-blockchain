async function main() {
  const FileRegistry = await ethers.getContractFactory("FileRegistry");
  const registry = await FileRegistry.deploy(); // deploy contract
  await registry.waitForDeployment(); // for Hardhat >= 2.20+
  
  const address = await registry.getAddress(); // get deployed address
  console.log(`FileRegistry deployed to: ${address}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});