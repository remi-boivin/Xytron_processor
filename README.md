# Xytron Spiking Neural Network (SNN) Processor 

![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/remi-boivin/spiking_processor?style=flat-square)
![GitHub License](https://img.shields.io/github/license/remi-boivin/spiking_processor?style=flat-square)
![GitHub Release](https://img.shields.io/github/v/release/remi-boivin/spiking_processor?sort=semver&display_name=release&style=flat-square)
![GitHub Repo stars](https://img.shields.io/github/stars/remi-boivin/spiking_processor?style=flat-square)
![GitHub forks](https://img.shields.io/github/forks/remi-boivin/spiking_processor?style=flat-square)

## Table of content
[Introduction](#introduction)
    [Key features](#key-features)
[Condition of use](#condition-of-use)
[Documentation](#documentation)
[Roadmap](#roadmap)
    [v0.1.0](#v010)
    [v0.2.0](#v020)
    [v0.3.0](#v030)
    [v0.4.0](#v040)
    [v0.5.0](#v050)
    [v1.0.0-beta](#v100-beta)

[References](#references)

## Introduction

Introduction to the Xytron Neuromorphic Processor

The Xytron Neuromorphic Processor represents a cutting-edge advancement in the field of artificial intelligence and neural computing. This processor is designed to emulate the brain's neural network functionality, offering an efficient and scalable solution for a wide range of applications, including machine learning, robotics, and real-time data processing.

At the heart of the Xytron Neuromorphic Processor is a versatile RISC-V core, an open-standard instruction set architecture known for its simplicity, modularity, and extensibility. The integration of the RISC-V core provides robust control and programmability, enabling precise management of the neuromorphic processing elements. This combination allows for the dynamic activation and configuration of neurons, tailoring the computational resources to specific tasks and enhancing overall system efficiency.

#### Key features:

- *Neuromorphic Computing Elements*: The processor incorporates leaky integrate-and-fire (LIF) neurons, which mimic the electrical characteristics of biological neurons. These elements facilitate complex neural computations with low power consumption.
- *Configurable Neural Network*: The RISC-V core enables fine-grained control over the neuromorphic elements, allowing users to activate or deactivate specific neurons and adjust their parameters. This flexibility supports a wide array of neural network architectures and learning algorithms.
 - *High Efficiency and Scalability*: Designed with a focus on energy efficiency, the Xytron Neuromorphic Processor leverages asynchronous event-driven processing to minimize power usage. The architecture is scalable, accommodating growth in network size and complexity without compromising performance.
- Versatile Interface: The processor supports a rich set of interfaces, including memory-mapped I/O and direct memory access (DMA), ensuring seamless integration with existing systems and facilitating the development of custom applications.

The Xytron Neuromorphic Processor is poised to drive innovation in intelligent systems, offering unparalleled performance and adaptability for next-generation computing challenges. By bridging the gap between conventional processing and neural-inspired computing, Xytron opens new possibilities for advancements in artificial intelligence and beyond.

In case you decide to use the Xytron HDL source code, we would appreciate if you let us know; **feedback is always welcome**.

# Condition of use

> *Digital HDL source code of Xytron is free: you can redistribute it and/or modify it under the terms of the Solderpad Hardware License v2.0, which extends the Apache v2.0 license for hardware use.*

> *The software, hardware and materials distributed under this license are provided in the hope that it will be useful on an **'as is' basis, without warranties or conditions of any kind, either expressed or implied; without even the implied warranty of merchantability or fitness for a particular purpose**. See the Solderpad Hardware License for more details.*

> *You should have received a copy of the Solderpad Hardware License along with the Xytron HDL files (see [LICENSE](LICENSE) file). If not, see <https://solderpad.org/licenses/SHL-2.0/>.*

## Documentation

> *The documentation for Xytron is under a Creative Commons Attribution 4.0 International License (see [doc/LICENSE](doc/LICENSE) file or http://creativecommons.org/licenses/by/4.0/).*

Documentation on the contents, usage and features of the Xytron HDL source code can be found in the [doc folder](doc/).

## Roadmap

- ### v0.1.0
    * Neurons can phenomenologically reproduce the LIF behavior.
    * Synapses embed spike-dependent synaptic plasticity (SDSP).
    * Basic simulation of the verilog modules.

- ### v0.2.0
    * Communication between the RISC-V core and the neurosynaptic core.
    * Memory mapped I/O.
    * Implement J-TAG interface.
    * Implement EEPROM interface.

- ### v0.3.0
    * Writing high level programs (C/C++, Python).
    * Xytron implement RISC-V core features.
        + Activate/Desactivate neurons in the neurosynaptic core through the RISC-V core.

- ### v0.4.0
    * Direct memory Access(DMA).
    * Neurosynaptic multi-core features.
        + Implement RISC-V parallelism mechanism for neurosynaptic multicore (choose which neurosynaptic core compute what).

- ### v0.5.0
    * RISC-V multi-core features.
    * RISC-V RTOS support.

- ### v1.0.0-beta
    * Neurons can phenomenologically reproduce the LIF behavior.
    * Synapses embed spike-dependent synaptic plasticity (SDSP)-based online learning
    * Xytron implement RISC-V core features.
        + Communication between the RISC-V core and the neurosynaptic core
        + Writing high level programs (C/C++, Rust, Python ...)
        + Activate/Desactivate neurons in the neurosynaptic core through the RISC-V core
    * Neurosynaptic multi-core features.
        + Implement RISC-V parallelism mechanism for neurosynaptic multicore (choose which neurosynaptic core process what)
    * Implement J-TAG interface.
    * Implement EEPROM interface.

## References

Inspired by this [paper](https://arxiv.org/pdf/1804.07858.pdf)):
> C. Frenkel, M. Lefebvre, J.-D. Legat and D. Bol, "A 0.086-mm² 12.7-pJ/SOP 64k-Synapse 256-Neuron Online-Learning Digital Spiking Neuromorphic Processor in 28-nm CMOS," *IEEE Transactions on Biomedical Circuits and Systems*, vol. 13, no. 1, pp. 145-158, 2019.