import type { Meta, StoryObj } from '@storybook/react';

import { Button } from './Button';

const meta = {
  title: 'Button',
  component: Button,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

// --- PRIMARY ---
export const PrimaryDefault: Story = {
  args: {
    label: 'Button',
    variant: 'primary',
    iconRight: 'ArrowRightBold',
  },
};

export const PrimaryLarge: Story = {
  args: {
    label: 'Button',
    size: 'large',
  },
};

export const PrimarySmall: Story = {
  args: {
    label: 'Button',
    size: 'small',
  },
};

export const PrimaryTiny: Story = {
  args: {
    label: 'Button',
    size: 'tiny',
  },
};

// --- SECONDARY ---
export const SecondaryDefault: Story = {
  args: {
    label: 'Button',
    variant: 'secondary',
  },
};

export const SecondaryLarge: Story = {
  args: {
    label: 'Button',
    variant: 'secondary',
    size: 'large',
  },
};

export const SecondarySmall: Story = {
  args: {
    label: 'Button',
    variant: 'secondary',
    size: 'small',
  },
};

export const SecondaryTiny: Story = {
  args: {
    label: 'Button',
    variant: 'secondary',
    size: 'tiny',
  },
};

// --- LINK ---
export const LinkDefault: Story = {
  args: {
    label: 'Button',
    variant: 'link',
  },
};

export const LinkLarge: Story = {
  args: {
    label: 'Button',
    variant: 'link',
    size: 'large',
  },
};

export const LinkSmall: Story = {
  args: {
    label: 'Button',
    variant: 'link',
    size: 'small',
  },
};

export const LinkTiny: Story = {
  args: {
    label: 'Button',
    variant: 'link',
    size: 'tiny',
  },
};
