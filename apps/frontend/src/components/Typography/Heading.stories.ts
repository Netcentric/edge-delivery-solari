import type { Meta, StoryObj } from '@storybook/react';

import { Heading } from './Typography';

const meta = {
  title: 'Heading',
  component: Heading,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<typeof Heading>;

export default meta;
type Story = StoryObj<typeof meta>;

export const H1: Story = {
  args: {
    level: 'h1',
    children: 'Heading h1',
  },
};
export const H2: Story = {
  args: {
    level: 'h2',
    children: 'Heading h2',
  },
};
export const H3: Story = {
  args: {
    level: 'h3',
    children: 'Heading h3',
  },
};
export const H4: Story = {
  args: {
    level: 'h4',
    children: 'Heading h4',
  },
};
export const H5: Story = {
  args: {
    level: 'h5',
    children: 'Heading h5',
  },
};
