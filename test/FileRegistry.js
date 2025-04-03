const { expect } = require("chai");

describe("FileRegistry", function () {
  let FileRegistry, registry;

  beforeEach(async function () {
    FileRegistry = await ethers.getContractFactory("FileRegistry");
    registry = await FileRegistry.deploy();
    // await registry.deployed();
  });

  it("should add and retrieve the latest file version", async function () {
    const filename = "example.txt";
    const hash1 = "abc123";

    await registry.addFileVersion(filename, hash1);

    const latest = await registry.getLatestFileVersion(filename);
    expect(latest.fileName).to.equal(filename);
    expect(latest.hash).to.equal(hash1);
    expect(latest.version).to.equal(1);
  });

  it("should increment version when a file is updated", async function () {
    const filename = "example.txt";
    const hash1 = "abc123";
    const hash2 = "def456";

    await registry.addFileVersion(filename, hash1);
    await registry.addFileVersion(filename, hash2);

    const latest = await registry.getLatestFileVersion(filename);
    expect(latest.hash).to.equal(hash2);
    expect(latest.version).to.equal(2);
  });

  it("should return all versions", async function () {
    const filename = "example.txt";
    const hash1 = "abc123";
    const hash2 = "def456";

    await registry.addFileVersion(filename, hash1);
    await registry.addFileVersion(filename, hash2);

    const allVersions = await registry.getAllVersions(filename);
    expect(allVersions.length).to.equal(2);
    expect(allVersions[0].hash).to.equal(hash1);
    expect(allVersions[1].hash).to.equal(hash2);
  });

  it("should fail when retrieving a file that does not exist", async function () {
    await expect(
      registry.getLatestFileVersion("nonexistent.txt")
    ).to.be.revertedWith("File not found");
  });
});
